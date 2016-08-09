import pandas as pd
import os
import getAlleleLists as gal

from itertools import compress




def fixallele(alleles):
    '''fix allele names'''
    if type(alleles) is not list:
        alleles = alleles.split(',')
    if type(alleles) is not list:
        alleles = list(alleles)
    return alleles


def annotation_score(row):
    ''' get annotation score '''
    row = list(row)
    idx = row.index(min(row))

    row.sort()
    score = row[1] / row[0]
    return round(score)


def getmin_allele(row):
    ''' get allele name with smallest binding concentrations '''
    tmp = list(row)
    idx = tmp.index(min(tmp))
    return ((row.axes[0]).values[idx])


def mywrite(file, seq):
    with open(file,'w') as f:
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



def prepare_for_NetMhcCons(workdir, pepseq, alleles, exe):
    files = writeSeqFilesForMHC(workdir, pepseq)
    alllist = gal.AlleleList()

    supportedalleles = alllist.findAll(alleles)
    commands = []
    outfiles = []
    for file in files:
        for allel in supportedalleles:
            outfile = os.path.splitext(file)[0]
            outfile += "_"
            outfile += allel.replace(":", "_")
            outfile += ".mhc"
            outfiles.append(outfile)

            command = "{exe} -inptype 1 -a {allel} -f {file} > {outfile}".format(exe=exe, allel=allel, file=file,
                                                                                 outfile=outfile)
            commands.append(command)
    return outfiles, commands


def concat_all_MHC_outputs(outfiles, df):
    outputs = []
    for file in outfiles:
        output2 = pd.read_csv(file, skipinitialspace=True, delimiter=" ", skiprows=range(0, 19) + [20], skipfooter=4,
                              engine='python')
        outputs.append(output2)

    allout = pd.concat(outputs)
    res = df.merge(allout, how='inner', left_on='search_hit', right_on='peptide')

    respiv = pd.pivot_table(res, index=list(df.columns), columns='Allele', values=u'Affinity(nM)')

    annotation_score_column = respiv.apply(annotation_score, axis=1)
    top_allele = respiv.apply(getmin_allele, axis=1)
    respiv['annotation_score'] = annotation_score_column
    respiv['top_allele'] = top_allele
    return respiv


if __name__ == "__main__":

    df = pd.read_csv('/home/systemhc/prog/SysteMHC_Data/peptideIDResult/PBMC1_Tubingen.csv',sep="\t", header=0)
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