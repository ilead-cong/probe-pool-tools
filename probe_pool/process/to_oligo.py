
def Add_seq(probe, add_seq):
    
    seq_list = add_seq.split(";")
    seq_l = seq_list[0]
    seq_r = seq_list[1]
    add_probe = seq_l + probe + seq_r
    return add_probe


from Bio.SeqUtils import MeltingTemp as mt
def Seq_tm_DNA(seq, salt_na=60, conc1=25, conc2=25, formconc=50):
    tm_original = mt.Tm_NN(seq, Na=salt_na, dnac1=conc1,
                           dnac2=conc2)
    tm_corrected = mt.chem_correction(tm_original, fmd=formconc)
    return tm_corrected


import nupack
nupack_model = nupack.Model(material="DNA", ensemble="stacking", 
                                celsius=117, sodium=0.39, 
                                magnesium=0.00)
def Probe_th(probe):
    
    # tm 
    tm = Seq_tm_DNA(probe)
    
    # fold
    
    
    prob_linear = nupack.structure_probability(strands=[probe], structure="."*len(probe), model=nupack_model)
    
    probe_fold = 1 - prob_linear
    
    return tm, probe_fold


