import random

def Eq_Space(in_tsv, number_desire, out_tsv):
    with open(in_tsv) as f:
        lines = f.readlines()
    n_lines = len(lines)
    #当探针总数小于期望数量时，跳过当前步骤20211106
    if n_lines <= number_desire:
        outlines = lines
    else:
        space = n_lines // number_desire
        outlines = [lines[i] for i in range(n_lines) if i % space == 0]
        while len(outlines) > number_desire:
            outlines.remove(random.choice(outlines))
    print(len(outlines))
    with open(out_tsv, 'w') as fo:
        for line in outlines:
            fo.write(line)