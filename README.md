# probe-pool-tools
A efficient, precise and fast probe design tools for DNA FISH.

## WORK PROCESS
This is the workflow of probe-tools-tools.

<img src=https://github.com/ilead-cong/probe-pool-tools/blob/main/figure/probe-pool-process.png width=40% />

## Enviroment

### Package list

1. python
2. Pyfaidx
3. Biopython
4. pandas
5. nupack

### New enviroment
Use conda create a new enviroment for probe-pool-tools and activate it.

```bash
conda create -n probe-pool-tools
conda activate probe-pool-tools
```

### Git the probe-pool-tools
Download probe-pool-tools from GitHub
```bash
git clone https://github.com/ilead-cong/probe-pool-tools
```

### Regular package installation
Most packages can be installed with conda

```bash
conda install python pyfaidx biopython pandas
```

### Special package installation
the installation of nupack should get the package from the [NUPACK official website](http://www.nupack.org/)


## Usage
Probe-pool-tools has two design patterns: normal and identify
### Normal
Design corresponding probes for a specific position of a single gene  

For example, using normal mode, design probes for the 100000-200000 region of human chromosome 1, the probe length is 70, and the interval is 50
```bash
python ./probe-pool-tools/run.py -dm normal -f hg19.fa -o ./ -pl 70 -ml 50  -t sample:hg19:chr1:100000-200000
```
### Identyfy
Designing discriminative probes between multiple species

For example, on the basis of the previous example, adding the ability of the probe to identify the mouse genome
```bash
python ./probe-pool-tools/run.py -dm identify -fd genomo_data_dir -ig mm10 -o ./ -pl 70 -ml 50  -t sample:hg19:chr1:100000-200000
```
### More usage
```bash
python ./probe-pool-tools/run.py -h 
usage: main.py [-h] -dm DESIGNMODEL -o OUTDIR -pl PROBELENGTH -ml MOVELENGTH
               -d DENSITY [-t TARGET] [-f FASTA] [-fd FASTADIR]
               [-ig IDENTIFYGENOME] [-eq EXPECTEDQUANTITY] [-kc KMERCUT]
               [-as ADDSEQ]

probe-pool-tools is a tools for DNA FISH probe design, tools version is 0.0.1

optional arguments:
  -h, --help            show this help message and exit
  -f FASTA, --fasta FASTA
                        the path of genome fasta file, like
                        "path/path/hg19.fa", when the model is "normal".
                        please make sure it has the same name with the input
                        target genome
  -fd FASTADIR, --fastadir FASTADIR
                        the path of alls genomes fasta directory, like
                        "path/path", when the model is "identify". please make
                        sure it has the same name with the input target genome
                        and identify genome
  -ig IDENTIFYGENOME, --identifygenome IDENTIFYGENOME
                        multiple identify genome,
                        like"genome_1;genome_2;...;genome_n" when the model is
                        "identify". please make sure it has the same name with
                        the file in fasta directory
  -eq EXPECTEDQUANTITY, --expectedquantity EXPECTEDQUANTITY
                        expected quantity, like 8000, If the final number
                        exceeds this number, perform probe homogenization;
                        otherwise, directly output all probes
  -kc KMERCUT, --kmercut KMERCUT
                        kmercut, like 5, If the count kmer of probe is big
                        than this number, this probe will be cutted
  -as ADDSEQ, --addseq ADDSEQ
                        addseq, like AATTCC;TTCCAA, Add primers to both ends
                        of the probe, LEFT;RIGHT

required arguments:
  -dm DESIGNMODEL, --designmodel DESIGNMODEL
                        Choose a design model; "normal" or "identify"
  -o OUTDIR, --outdir OUTDIR
                        result output directory, like "path/path"
  -pl PROBELENGTH, --probelength PROBELENGTH
                        the length of probe, like 70
  -ml MOVELENGTH, --movelength MOVELENGTH
                        The distance between the starting positions of the
                        candidate probes, or the moving distance, like 50
  -d DENSITY, --density DENSITY
                        The distance between the starting positions of the
                        candidate probes, or the moving distance, like 5e-5
  -t TARGET, --target TARGET
                        target information, composed by name:genome:chr:start-
                        end, like"sample:hg19:chr1:100000-200000"
```
## Result description
The process outputs 6 folders and a file
|  name   | content  |
|  ----  | ----  |
| 00-pregenome   | Results of genome preprocessing, including new reference genomes, Bowtie2-index, kmer databases |
| 01-target_fa   | The sequence of target region wiht fasta file |
| 02-probe_fq   | candidate probes wiht fastq file |
| 03-probe_sam   | Alignment results of candidate probes |
| 04-probe_tsv   | Intermediate files for probe filtering, including OTP filtering and kmer filtering |
| 05-qc   | Intermediate file for the quality control process of the resulting probe |
| sample.oligo   | Probe file |

## More infomation
If you encounter any errors or other problems, please send an email to pluaron at w2628705328@gmail.com.
