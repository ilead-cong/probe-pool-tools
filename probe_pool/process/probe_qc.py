
import typing as t
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

def fq_recs(f):
    for line in f:
        items = line.strip().split("\t")
        yield items[0], items[1], "~"*len(items[1])

def Tsv_to_fq(tsv_path, fq_path):
    with open(tsv_path) as f:
        Write_fq(fq_path, fq_recs(f))
