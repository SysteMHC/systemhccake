import numpy as np
import pandas as pd
import os

df = pd.read_csv('/home/witold/prog/systeMHC/documentation/input_v2_elife.txt',sep="\t",header=1,skiprows=0)

df.columns
df.shape


for i in df['MHC Allele']:
    print i.split(',')

os.listdir('/home/witold/prog/systeMHC/documentation')

def mywrite(txt, seq):
    with open(txt,'w') as f:
        for item in seq:
            f.write("%s\n" % item)

print df.head()
df = pd.read_csv('/home/witold/prog/tests/1602031340/IprohetPepXML2CSV/PBMC1_Tubingen.csv',sep="\t", header=0)

df.drop_duplicates('modified_peptide','assumed_charge').shape



df.to_csv('peptides.csv' ,columns=[u'search_hit'],index=False,header=False)



txt = "/home/witold/prog/SysteMHC_Binaries/netMHCcons/netMHCcons-1.1/test/test8.pep"

def maketxtfile(path, stem, extension, peplength):
    filepath = os.path.join(path,"{stem}{peplength}.{extension}".format(stem=stem,peplength=peplength, extension=extension))
    return filepath


def extract_peptide_length(peplength, txtfile):
    df8 = df[df['search_hit'].map(len) == peplength]
    seq = df8['search_hit'].tolist()
    seq = set(seq)
    mywrite(txtfile, seq)


output2 = pd.read_csv('test8.cons.B78.txt', skipinitialspace =True, delimiter=" ", skiprows=range(0,19) + [20], skipfooter=4,engine='python')


'''

- inputs peptide csv file result of a single search
- a list of alleles

For all allelles in the list and all pepitde lengths run netMHCcons

write all peptides with given sequence 8 - 15
call netMHCcons with a list of alleles

read all peptides with given sequence

'''