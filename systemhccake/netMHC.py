from applicake.base.app import WrappedApp
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
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument("NETMHCCONS",
                     KeyHelp.EXECDIR,
                     default='{}/SysteMHC_Binaries/netMHCcons/netMHCcons-1.1/netMHCcons'.format(os.environ.get('SYSTEMHC'))),
            Argument("ALLELE_LIST", 'list of alleles', default=''),
            Argument('PEPCSV', 'Table with ids', default=''),
        ]

    def prepare_run(self, log, info):
        wd = info[Keys.WORKDIR]

        iprophoutput = info['PEPCSV']
        alleles = info['ALLELE_LIST']
        exe = info['NETMHCCONS']

        self.df = pd.read_csv(iprophoutput,sep="\t", header=0)
        uniqueSeq = self.df.drop_duplicates(subset=['search_hit'])
        pepseq = uniqueSeq['search_hit'].tolist()
        files = pso.writeSeqFilesForMHC(wd , pepseq)

        alllist = gal.AlleleList()
        supportedalleles = alllist.findAll(alleles)

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

        outputs = []

        for file in self.outfiles:
            log.debug(file)
            output2 = pd.read_csv(file, skipinitialspace =True, delimiter=" ", skiprows=range(0,19) + [20], skipfooter=4,engine='python')
            outputs.append(output2)

        allout = pd.concat(outputs)
        res = self.df.merge(allout, how='inner', left_on='search_hit', right_on='peptide')
        respiv = pd.pivot_table(res,index=list(self.df.columns), columns='Allele', values=u'Affinity(nM)')


        info['NETMHC_OUT'] = os.path.join(info[Keys.WORKDIR], 'netmhccons.output.csv')

        respiv.to_csv(info['NETMHC_OUT'], sep="\t")

        # get all the generated outptuts
        return info


if __name__ == "__main__":
    sys.argv = ['--ALLELE_LIST', 'A03,A24,B07,B51', '--PEPCSV', '/home/systemhc/prog/systemhccake/tests/PBMC1_Tubingen.csv']
    NetMHC.main()
