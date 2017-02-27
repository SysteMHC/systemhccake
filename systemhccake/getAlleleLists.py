import os
import pandas as pd
import re

os.environ['SYSTEMHC'] = '/home/systemhc/prog'

class AlleleList:

    def __init__(self, dirNetMHC='{}/SysteMHC_Binaries/netMHC/netMHC-3.4/etc/net'.format(os.environ.get('SYSTEMHC')),
                 dirNetPan='{}/SysteMHC_Binaries/netMHCpan/netMHCpan-2.8/data/MHC_pseudo.dat'.format(os.environ.get('SYSTEMHC'))
    ):

#    def __init__(self,
#                dirNetMHC='/home/systemhc/prog/SysteMHC_Binaries/netMHC/netMHC-3.4/etc/net',
#                dirNetPan='/home/systemhc/prog/SysteMHC_Binaries/netMHCpan/netMHCpan-2.8/data/MHC_pseudo.dat'
#    ):

        self.mhcAlleles =[]
        self.netMHCalleles = os.listdir(dirNetMHC)
        df = pd.read_csv(dirNetPan,delimiter=r"\s+", header=None)
        self.netPanalleles= list(set(df[0].tolist()))


    @staticmethod
    def findAllS(alleles, netAll, prefix = "HLA-"):
        filall = []
        for all in alleles:
            all = prefix + all
            print all
            matches =  filter( lambda x : all in x , netAll)
            filall.append(re.sub("_.+$","",matches[0])) # take first match only
        return filall

    def findAll(self, alleles):
        self.mhcAlleles= AlleleList.findAllS(alleles, self.netMHCalleles + self.netPanalleles)
        return self.mhcAlleles


    def show(self):
        for i in self.mhcAlleles:
            print i




if __name__ == "__main__":
    from systemhccake.getAlleleLists import AlleleList

    alllist = AlleleList()
    all = ['A03', 'A24', 'B07', 'B51']
    supportedalleles = alllist.findAll(all)
    print supportedalleles
    alllist.show()