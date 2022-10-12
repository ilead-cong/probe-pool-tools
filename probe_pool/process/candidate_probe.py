# pluaron
# 20221009
# extract candidate probes from target sequence

import typing as t

from pyfaidx import Fasta


def To_fq_rec(rec: t.Tuple[str, str, int, int]) -> t.Tuple[str, str, str]:
    seq, name, s, e = rec
    seqname = f"{name}:{s}_{e}"
    qualstr = "~"*len(seq)
    return seqname, seq, qualstr

def Write_fq(
        path: str,
        g: t.Iterable[t.Tuple[str, str, str]]) -> str:
    """Write contents in sub-sequence generator to fastq file.

    :param path: Target fastq file.
    :param g: sub-sequences generator.
    :return: output fastq path.
    """
    with open(path, 'w') as f:
        for seqname, seq, qualstr in g:
            f.write("@"+seqname+"\n")
            f.write(seq+"\n")
            f.write("+\n")
            f.write(qualstr+"\n")
    return path

def Fa_seq_read(fasta_file):
   fa = Fasta(fasta_file)
   for key in fa.keys():
       name = key
       seq = fa[key][:].seq
       yield name, seq

def Slide_through(seq: str,
                  sub_len: int,
                  overlap: int) -> t.Iterable[t.Tuple[str, int, int]]:
    """Slide through a sequence, generate it's subsequences.

    :param seq: Input sequence.
    :param sub_len: Length of sub-sequence.
    :param overlap: Overlap size between two sub-sequences.
    :return: Generator of a tuple of sub-sequences,
    and it's start and end position in original sequence.
    """
    assert sub_len > 0, "sub-sequence length must large than zero."
    assert overlap >= 0, 'overlap length must large or equal to zero.'
    assert overlap < sub_len, 'overlap length must less than sub-seq length.'
    step = sub_len - overlap
    tlen = len(seq)
    sub_start = 0
    while sub_start + sub_len <= tlen:
        sub_end = sub_start + sub_len
        sub_seq = seq[sub_start:sub_end]
        yield sub_seq, sub_start, sub_end
        sub_start += step

def Slide_through_fasta(path: str,
                        slen: int,
                        overlap: int) -> t.Iterable[t.Tuple[str, str, int, int]]:
    """Slide through all sequences in fasta file.

    :param path: Input fasta file.
    :param slen: Length of sub-sequence.
    :param overlap: Overlap size between two sub-sequences.
    :return: Generator of a tuple of sub-sequences,
    and it's seq-name and start, end position in original sequence.
    """
    
    for name, seq in Fa_seq_read(path):
        for sub_seq, sub_start, sub_end in Slide_through(seq, slen, overlap):
            yield sub_seq, name, sub_start, sub_end



def Candidates(in_file: str,
               out_file: str,
               length: int,
               overlap: int):
    gen = Slide_through_fasta(in_file, length, overlap)
    gen = map(To_fq_rec, gen)
    Write_fq(out_file, gen)