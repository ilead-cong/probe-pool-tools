# pluaron
# 20221009
# Preprocessing of reference and discriminant genomes


'''
Identifying model:
1.renaming and merging of multiple genomes 
2.Bowtie2 index building with new genome

out_dir = 00-genome-data
'''

from probe_pool.tools.subprocess_call import Subp_call
def Genome_pre(identify_genome, fasta_dir, out_dir):
    result_fa = f"{out_dir}/all.fa"
    ig_list = identify_genome.split(",")
    ig_file_list = []
    # add ig name in the front of chrn
    for ig in ig_list:
        ig_file = f"{fasta_dir}/{ig}.fa"
        ig_file_list.append(ig_file)
        sed_str = f"s,>,>{ig}_,g"
        ig_cmd = f"sed -i '{sed_str}' {ig_file}"
        Subp_call(ig_cmd)
        
    # Merge files
    cat_str = " ".join(ig_file_list)
    cat_cmd = f"cat {cat_str} > {result_fa}"
    Subp_call(cat_cmd)

    return

# change the target information
def Target_add(target):
    target_list = target.split(":")
    genome = target_list[1]
    chrn = target_list[2]
    location = target_list[3]
    target_add = f"{genome}_{chrn}:{location}"
    return target_add
