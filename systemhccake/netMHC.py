from applicake.base.app import WrappedApp
#from applicake.base.apputils import validation
from applicake.base.coreutils.arguments import Argument
from applicake.base.coreutils.keys import Keys, KeyHelp
import pandas as pd
from applicake.base.apputils.validation import check_exitcode, check_xml

import parseSearchOutput as pso
import getAlleleLists as gal

import os
import sys




class NetMHC(WrappedApp):
    outfiles=[]

    def add_args(self):
        return [
            Argument("NETMHCCONS",  KeyHelp.EXECDIR, default='/home/witold/prog/SysteMHC_Binaries/netMHCcons/netMHCcons-1.1/netMHCcons'),
            Argument("ALLELE_LIST", 'list of alleles', default=''),
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument('IPROPHETOUTPUT', 'Table with ids', default=''),
        ]

    def prepare_run(self, log, info):
        wd = info[Keys.WORKDIR]

        iprophoutput = info['IPROPHETOUTPUT']
        alleles = info['ALLELE_LIST']
        exe = info['NETMHCCONS']


        df = pd.read_csv(iprophoutput,sep="\t", header=0)
        uniqueSeq = df.drop_duplicates(subset=['search_hit'])
        pepseq = uniqueSeq['search_hit'].tolist()
        files = pso.writeSeqFilesForMHC(wd , pepseq)

        alllist = gal.AlleleList()
        alleles = alleles.split(",")
        supportedalleles = alllist.findAll(alleles)

        #./netMHCcons/netMHCcons-1.1/netMHCcons -inptype 1 -a HLA-B78:07 -f /home/witold/prog/SysteMHC_Binaries/netMHCcons/netMHCcons-1.1/test/test8.pep
        #./netMHCcons/netMHCcons-1.1/netMHCcons -inptype 1 -a HLA-B78:07 -f ./netMHCcons/netMHCcons-1.1/test/test2.pep > ./netMHCcons/netMHCcons-1.1/test/test2.pep.myout
        commands  = []
        for file in files:
            for allel in supportedalleles:
                outfile = os.path.splitext(file)[0]
                outfile += "_"
                outfile += allel.replace(":", "_")
                outfile += ".mhc"
                self.outfiles.append(outfile)

                command = "{exe} -inptype 1 -a {allel} -f {file} > {outfile}".format(exe=exe, allel=allel, file=file, outfile=outfile)
                commands.append(command)

        return info, commands


    def validate_run(self, log, info, exit_code, stdout):
        check_exitcode(log,exit_code)
        #print self.outfiles
        for i in self.outfiles:
            log.debug(i)
        # get all the generated outptuts
        return info


if __name__ == "__main__":
    sys.argv = ['--ALLELE_LIST', 'A03,A24,B07,B51', '--IPROPHETOUTPUT', '/home/witold/prog/SysteMHC_Data/peptideIDResult/PBMC1_Tubingen.csv']
    #sys.argv = ['--ALLELE_LIST', 'A03', '--IPROPHETOUTPUT', '/home/witold/prog/SysteMHC_Data/peptideIDResult/PBMC1_Tubingen.csv']

    NetMHC.main()
