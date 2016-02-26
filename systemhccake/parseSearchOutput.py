import glob

import pandas as pd
import os
from itertools import compress

def mywrite(txt, seq):
    with open(txt,'w') as f:
        for item in seq:
            f.write("%s\n" % item)


def maketxtfile(path, stem, extension, peplength):
    filepath = os.path.join(path,"{stem}{peplength}.{extension}".format(stem=stem,peplength=peplength, extension=extension))
    return filepath


def extract_peptide_length(pepseq, peplength):
    idxB = map(lambda x : len(x) == peplength, pepseq)
    pepseq = list(compress(pepseq,idxB))
    return pepseq


def writeSeqFilesForMHC(path, pepseq):
    res = []
    sum = 0
    for peplength in range(8, 16):
        newseq = extract_peptide_length(pepseq, peplength)
        sum += len(newseq)
        fck = maketxtfile(path,'pep','txt',peplength)
        mywrite(fck,newseq)
        res.append(fck)
    print "{} == {} ".format(sum, len(pepseq))
    return res



if __name__ == "__main__":

    df = pd.read_csv('/home/witold/prog/SysteMHC_Data/peptideIDResult/PBMC1_Tubingen.csv',sep="\t", header=0)
    uniqueSeq = df.drop_duplicates(subset=['search_hit'])
    pepseq = uniqueSeq['search_hit'].tolist()
    files=  writeSeqFilesForMHC("./systemhccake/",pepseq)


    df.to_csv('peptides.csv' ,columns=[u'search_hit'],index=False,header=False)


    txt = "/home/witold/prog/SysteMHC_Binaries/netMHCcons/netMHCcons-1.1/test/test8.pep"






'''

- inputs peptide csv file result of a single search
- a list of alleles

For all allelles in the list and all pepitde lengths run netMHCcons

write all peptides with given sequence 8 - 15
call netMHCcons with a list of alleles

read all peptides with given sequence

'''