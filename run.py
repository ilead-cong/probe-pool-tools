# pluaron
# 20221009
# probe pool design
import argparse


from probe_pool.tools.make_dir import Mk_not_dir
from probe_pool.tools.subprocess_call import Subp_call
from probe_pool.process.pregenome import Genome_pre, Target_add
from probe_pool.process.candidate_probe import Candidates
from probe_pool.process.equal_space import Eq_Space
from probe_pool.process.probe_qc import Tsv_to_fq
from probe_pool.process.kmer_filter import Tsv_to_fa, Kmer_analysis
from probe_pool.process.to_oligo import Add_seq, Probe_th

tools_name="probe-pool-tools"
tools_version = "0.0.1"



def main():
    
    # Allow user to input parameters on command line.
    tools_params = argparse.ArgumentParser(description=f"{tools_name} is a tools for FISH probe design, tools version is {tools_version}")
    required_params = tools_params.add_argument_group('required arguments')
    required_params.add_argument('-dm', '--designmodel', action='store', required=True,
                               help='Choose a design model; "normal" or "identify"')
    required_params.add_argument('-o', '--outdir', action='store', required=True,
                               default='.', type=str,
                               help='result output directory, like "path/path"')
    required_params.add_argument('-pl', '--probelength', action='store', required=True,
                               default=70, type=int,
                               help='the length of probe, like 70')
    required_params.add_argument('-ml', '--movelength', action='store', required=True,
                               default=50, type=int,
                               help='The distance between the starting positions of the candidate probes, \
                                   or the moving distance, like 50')
    required_params.add_argument('-d', '--density', action='store', required=True,
                               default="5e-5", type=str,
                               help='The distance between the starting positions of the candidate probes, \
                                   or the moving distance, like 5e-5')
    required_params.add_argument('-t', '--target', action='store', type=str,
                               help='target information, composed by name:genome:chr:start-end,\
                                   like"sample:hg19:chr1:100000-200000"')
    tools_params.add_argument('-f', '--fasta', action='store', type=str,
                               help='the path of genome fasta file, like "path/path/hg19.fa",\
                               when the model is "normal". please make sure it has the same name \
                                   with the input target genome')
    tools_params.add_argument('-fd', '--fastadir', action='store', type=str,
                               help='the path of alls genomes fasta directory, like "path/path",\
                               when the model is "identify". please make sure it has the same name \
                                   with the input target genome and identify genome')
    tools_params.add_argument('-ig', '--identifygenome', action='store',
                           type=str, help='multiple identify genome, like"genome_1;genome_2;...;genome_n" \
                               when the model is "identify". please make sure it has the same name \
                                   with the file in fasta directory')
    tools_params.add_argument('-eq', '--expectedquantity', action='store',
                           type=int, default=0,
                           help='expected quantity, like 8000, \
                               If the final number exceeds this number, \
                                   perform probe homogenization; otherwise, directly output all probes')
    tools_params.add_argument('-kc', '--kmercut', action='store',
                           type=int, default=5,
                           help='kmercut, like 5, \
                               If the count kmer of probe is big than this number, \
                                   this probe will be cutted')
    tools_params.add_argument('-as', '--addseq', action='store',
                           type=str, default="",
                           help='addseq, like AATTCC;TTCCAA, \
                               Add primers to both ends of the probe, LEFT;RIGHT')
    

    # Import user-specified command line values.
    args = tools_params.parse_args()
    design_model = args.designmodel
    out_dir = args.outdir
    genome_fa = args.fasta
    ig_str = args.identifygenome
    fa_dir = args.fastadir
    target = args.target
    probe_len = args.probelength
    probe_move = args.movelength
    density = eval(args.density)
    eq_number = args.expectedquantity
    kmer_cut = args.kmercut
    add_seq = args.addseq
    
    
    # other param
    jf_len = int(probe_len / 2)
    
    
    #start
    Mk_not_dir(out_dir)
    sample_name = target.split(":")[0]

    
    # 00-pregenome
    pre_dir = f"{out_dir}/00-pregenome"
    Mk_not_dir(pre_dir)
    # normal
    if design_model == "normal":
        print("use normal design model")
        Subp_call(f"cp {genome_fa} {pre_dir}/all.fa")
        target_list = target.split(":")
        chrn = target_list[2]
        location = target_list[3]
        target_add = f"{chrn}:{location}"
    # identify
    elif design_model == "identify":
        print("use identify model")
        Genome_pre(identify_genome=ig_str, fasta_dir=fa_dir, out_dir=pre_dir)
        target_add = Target_add(target)
    else:
        print(" design model parameter wrong!")
    # genome_file_path
    genome_file = f"{pre_dir}/all.fa"
    
    # make bowtie2 index
    index_dir = f"{pre_dir}/bowtie2-index"
    index_log = f"{pre_dir}/index.log"
    Mk_not_dir(index_dir)
    index_cmd = f"bowtie2-build {genome_file} {index_dir}/all > {index_log} 2>&1"
    Subp_call(index_cmd)
    
    # make kmer jf
    jf_file = f"{pre_dir}/all.jf"
    jf_cmd = f"jellyfish count -m {jf_len} -s 64 -o {jf_file} {genome_file}"
    Subp_call(jf_cmd)
    
    
    
    # 01-target_fa
    tar_dir = f"{out_dir}/01-target_fa"
    Mk_not_dir(tar_dir)
    extract_cmd = f"faidx {genome_file} {target_add} > {tar_dir}/{sample_name}.fa"
    Subp_call(extract_cmd)
    
    
    
    
    # 02-probe_fq
    pro_dir = f"{out_dir}/02-probe_fq"
    Mk_not_dir(pro_dir)
    probe_set = f"{pro_dir}/{sample_name}.fq"
    # extract candidate probes
    Candidates(genome_file, probe_set, probe_len, probe_move)
    
    
    
    
    #03-probe_sam
    sam_dir = f"{out_dir}/03-probe_sam"
    Mk_not_dir(sam_dir)
    probe_sam = f"{sam_dir}/{sample_name}.sam"
    sam_log = f"{sam_dir}/{sample_name}_sam.log"
    sam_cmd = f"bowtie2 -x {index_dir}/all -U {probe_set} -t -k 100 --very-sensitive-local -S {probe_sam} > {sam_log} 2>&1"
    Subp_call(sam_cmd)
    
    
    
    
    #04-probe_tsv
    # otp
    tsv_dir = f"{out_dir}/04-probe_tsv"
    Mk_not_dir(tsv_dir)
    otp_file = f"./probe-pool-tools/probe_pool/process/OTP_filter"
    probe_tsv = f"{tsv_dir}/{sample_name}.tsv"
    tsv_cmd = f"{otp_file} {probe_sam} {probe_tsv} {target_add} {density}"
    Subp_call(f"chmod 777 {otp_file}")
    Subp_call(tsv_cmd)
    
    # kmer filter
    kmer_fa = f"{tsv_dir}/{sample_name}.fa"
    Tsv_to_fa(probe_tsv, kmer_fa)
    kmer_result = f"{tsv_dir}/{sample_name}_kmer.tsv"
    kmer_probe = f"{tsv_dir}/{sample_name}_kmercut.tsv"
    kmer_cmd = f"jellyfish query {jf_file} -s {kmer_fa} -o {kmer_result}"
    Subp_call(kmer_cmd)
    Kmer_analysis(kmer_fa, kmer_result, probe_tsv, kmer_probe, kmer_cut)
    
    # equal space
    probe_tsv_eq = f"{tsv_dir}/{sample_name}_eq.tsv"
    if eq_number == 0:
        Subp_call(f"cp {kmer_probe} {probe_tsv_eq}")
    else:
        Eq_Space(kmer_probe, eq_number, probe_tsv_eq)
    
    
    
    
    #05-qc
    qc_dir = f"{out_dir}/05-qc"
    Mk_not_dir(qc_dir)
    qc_fq = f"{qc_dir}/{sample_name}_qc.fq"
    qc_sam = f"{qc_dir}/{sample_name}_qc.sam"
    qc_bam = f"{qc_dir}/{sample_name}_qc.bam"
    qc_cov = f"{qc_dir}/{sample_name}_qc.cov"
    Tsv_to_fq(probe_tsv_eq, qc_fq)
    Subp_call(
            f"bowtie2 -x {index_dir}/all -U {qc_fq} -t -k 100 --very-sensitive-local -S {qc_sam} && " + \
            f"sambamba view -f bam -S -t 1 {qc_sam} | samtools sort -@ 1 > {qc_bam} && " +\
            f"samtools index {qc_bam}"
            )
    Subp_call(
            f"samtools coverage -r {target_add} {qc_bam} > {qc_cov}"
    )
    
    
    
    
    
    # 06-oligo
    # qc
    with open(qc_cov, "r") as f1:
        for line in f1.readlines()[1:]:
            line_list = line.strip().split("\t")
            number_probe = line_list[3]
            cov_probe = line_list[5]
    #time
    import time
    localtime = time.asctime(time.localtime(time.time()))
    # identify genome
    if design_model == "identify":
        oligo_ig = ig_str
    else:
        oligo_ig = ""
    
    
    # header
    oligo_file = f"{out_dir}/{sample_name}.oligo"
    f0 = open(oligo_file, "w")
    f0.write(f"#{localtime}" + "\n")
    f0.write(f"#{target}" + "\n")
    f0.write(f"#{cov_probe}:{number_probe}:{probe_len}-{probe_move}" + "\n")
    f0.write(f"#Bowtie2:{sam_cmd}" + "\n") 
    f0.write(f"#{oligo_ig}" + "\n")
    f0.write(f"#kmer:{jf_len};{kmer_cut}" + "\n")
    # probe
    f0.write("name\tsequence\tTm\tFoldScore\tPrimerSequence\tCountTarget\tCountOutTarget\tTargetScore\n")
    with open(probe_tsv_eq, "r") as f2:
        for line in f2:
            line_list = line.strip().split("\t")
            name = line_list[0]
            seq = line_list[1]
            tm, fold = Probe_th(seq)
            if add_seq:
                primer_probe = Add_seq(seq, add_seq)
            else:
                primer_probe = ""
            count_target = line_list[2]
            count_out_target = line_list[3]
            if eval(line_list[3]) == 0:
                target_score = "*"
            else:
                target_score = line_list[4]
            
            list_write = [name, seq, tm, fold, primer_probe, count_target, count_out_target, target_score]
            str_write = "\t".join(list_write)
            f0.write(str_write + "\n")
    
    f0.close()
    
    
    return




if __name__ == "__main__":
    main()
