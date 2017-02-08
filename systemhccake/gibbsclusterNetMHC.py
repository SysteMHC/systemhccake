import pandas as pd
from applicake2.base.app import WrappedApp
from applicake2.base.coreutils.arguments import Argument
from applicake2.base.coreutils.keys import Keys, KeyHelp
from applicake2.base.apputils.validation import check_exitcode
import parseSearchOutput as pso
import os
import sys

from gibbscluster import fixStupidGibbsclusterFile, runweblogo_on_files

def prepare_for_Gibscluster2(exe, workdir, pepseq, length=8):
    commands = []
    outfiles = []

    for key, pepseq in pepseq.items():
        print key
        key = key.replace(":", "-")
        fck = pso.maketxtfile(workdir, 'gibbs_in_', 'pep', key)
        pso.mywrite(fck, pepseq)

        outfile = pso.maketxtfile(workdir, 'gibbs_out_', 'gibbs', key)
        command = "{exe} -fast -l {length} -s -1 {infile} > {outfile}".format(exe=exe,
                                                                              length=length,
                                                                              infile=fck,
                                                                              outfile=outfile)

        outfiles.append(outfile)
        commands.append(command)
    return outfiles, commands

class GibbsClusterNETHMC(WrappedApp):
    outfiles = []

    def add_args(self):
        return [
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument("GIBSCLUSTER",
                     KeyHelp.EXECDIR,
                     default='{}/SysteMHC_Binaries/gibbscluster-1.1/gibbscluster'.format(os.environ.get('SYSTEMHC'))),
            Argument("WEBLOGO",
                     KeyHelp.EXECDIR,
                     default='{}/SysteMHC_Binaries/weblogo/weblogo'.format(os.environ.get('SYSTEMHC'))),
            Argument('NETMHC_OUT', 'NetMHC output', default=''),
        ]

    def prepare_run(self, log, info):
        sysmhcdir = os.environ.get('SYSTEMHC')

        if sysmhcdir is None:
            log.warning("systemhc not set")
        else:
            log.info('systemhc directory is: ' + sysmhcdir)

        workdir = info[Keys.WORKDIR]
        nethmhcout = info['NETMHC_OUT']

        exegibbs = info['GIBSCLUSTER']

        self.df = pd.read_csv(nethmhcout, sep="\t", header=0)
        top_alleles = self.df['top_allele']
        top_all = top_alleles.drop_duplicates().tolist()

        pepseq = {}
        for allele in top_all:
            pepseq[allele] = list(set((self.df[self.df['top_allele'] == allele]['search_hit']).tolist()))

        self.outfiles, commands = prepare_for_Gibscluster2(exegibbs, workdir, pepseq)
        return info, commands

    def validate_run(self, log, info, exit_code, stdout):
        check_exitcode(log, exit_code)

        weblogoexe = info['WEBLOGO']

        weblogoinputs = []
        for file in self.outfiles:
            weblogoinputs += fixStupidGibbsclusterFile(file, file + "out")

        commands = runweblogo_on_files(weblogoexe, weblogoinputs)
        self.execute_run(log, info, commands)

        return info


if __name__ == "__main__":
    sys.argv = ['--NETMHC_OUT', '/home/systemhc/prog/systemhccake/tests/netmhccons.output.csv']
    GibbsClusterNETHMC  .main()
