

def Tsv_to_fa(tsv_file, fa_file):
    
    f1 = open(fa_file, "w")
    with open(tsv_file, "r") as f2:
        for line in f2:
            line_list = line.strip().split("\t")
            name = f">{line_list[0]}"
            seq = line_list[1]
            f1.write(name + "\n" + seq + "\n")
    
    f1.close()
    
    return

from pyfaidx import Fasta
import pandas as pd
def Kmer_analysis(fa_file, result_tsv, probe_tsv, out_tsv, kmer_cut):
    
    dict_probe = {}
    with open(probe_tsv, "r") as f3:
        for line in f3:
            line_list = line.strip().split("\t")
            probe_name = line_list[0]
            dict_probe[probe_name] = line
    
    fa = Fasta(fa_file)
    list_fa = list(fa.keys())
    seq_number = len(fa.keys())
    
    df = pd.read_csv(result_tsv, sep=" ", header=None)
    list_res = list(df[1])
    len_res = len(list_res)
    
    pace = int(len_res / seq_number)
    
    with open(out_tsv, "w") as f2:
        start = 0
        for name in list_fa:
            seq_kmer = max(list_res[start:start+pace])
            start = start + pace
            if seq_kmer <= kmer_cut:
                f2.write(dict_probe[name] + "\n")
    return