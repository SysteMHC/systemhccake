import os
import glob
import pandas as pd

os.listdir("../tests")
files = glob.glob("./tests/*.mhc")
print files

outputs = []


for file in files:
    output2 = pd.read_csv(file, skipinitialspace =True, delimiter=" ", skiprows=range(0,19) + [20], skipfooter=4,engine='python')
    outputs.append(output2)

allout = pd.concat(outputs)

df = pd.read_csv('/home/witold/prog/SysteMHC_Data/peptideIDResult/PBMC1_Tubingen.csv',sep="\t", header=0)



df.shape
df.columns
allout.shape

allout.columns

res = df.merge(allout, how='inner', left_on='search_hit', right_on='peptide')


respiv = pd.pivot_table(res,index=list(df.columns), columns='Allele', values=u'Affinity(nM)')
respiv.head()
respiv.shape
res.head()
respiv.to_csv("./tests/symbolicnetmhccons.ouptut.csv",sep="\t")