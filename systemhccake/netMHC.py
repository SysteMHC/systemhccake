from applicake.base.app import WrappedApp
from applicake.base.coreutils.arguments import Argument
from applicake.base.coreutils.keys import Keys, KeyHelp
import pandas as pd
from applicake.base.apputils.validation import check_exitcode
import parseSearchOutput as pso
import os
import sys


class NetMHC(WrappedApp):
    outfiles=[]
    def add_args(self):
        return [
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument("NETMHCCONS",
                     KeyHelp.EXECDIR,
                     default='{}/SysteMHC_Binaries/netMHCcons/netMHCcons-1.1/netMHCcons'.format(os.environ.get('SYSTEMHC'))),
            Argument("ALLELE_LIST", 'list of alleles', default=''),
            Argument('PEPCSV', 'Table with ids', default=''),
        ]


    def prepare_run(self, log, info):
        workdir = info[Keys.WORKDIR]
        iprophoutput = info['PEPCSV']
        alleles = pso.fixallele(info['ALLELE_LIST'])

        exe = info['NETMHCCONS']

        self.df = pd.read_csv(iprophoutput,sep="\t", header=0)
        uniqueSeq = self.df.drop_duplicates( subset=['search_hit'] )
        pepseq = uniqueSeq['search_hit'].tolist()

        self.outfiles, commands = pso.prepare_for_NetMhcCons(workdir, pepseq, alleles, exe)

        return info, commands


    def validate_run(self, log, info, exit_code, stdout):
        check_exitcode(log,exit_code)

        respiv = pso.concat_all_MHCOutputs(self.outfiles, self.df)
        info['NETMHC_OUT'] = os.path.join(info[Keys.WORKDIR], 'netmhccons.output.csv')

        respiv.to_csv(info['NETMHC_OUT'], sep="\t")

        # get all the generated outptuts
        return info


if __name__ == "__main__":
    sys.argv = ['--ALLELE_LIST', 'A03,A24,B07,B51', '--PEPCSV', '/home/systemhc/prog/systemhccake/tests/PBMC1_Tubingen.csv']
    NetMHC.main()
