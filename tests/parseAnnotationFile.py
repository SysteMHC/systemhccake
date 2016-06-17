import pandas as pd
df = pd.read_csv('/home/witold/prog/systeMHC/documentation/input_v2_elife.txt',sep="\t",header=1,skiprows=0)

df.columns
df.shape
print df.head()

for i in df['MHC Allele']:
    print i.split(',')

