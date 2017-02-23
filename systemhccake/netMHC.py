from applicake.base.app import WrappedApp
from applicake.base.coreutils.arguments import Argument
from applicake.base.coreutils.keys import Keys, KeyHelp
from applicake.base.apputils.validation import check_exitcode
import parseSearchOutput as pso
import pandas as pd
import os
import sys
import subprocess


os.environ['SYSTEMHC'] = '/home/systemhc/prog'




class NetMHC(WrappedApp):
    outfiles=[]
    def add_args(self):
        return [
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument("NETMHCCONS",
                     KeyHelp.EXECDIR,
                     default='{}/SysteMHC_Binaries/netMHCcons/netMHCcons-1.1/netMHCcons'.format(os.environ.get('SYSTEMHC'))),
                     #default='/home/systemhc/prog/SysteMHC_Binaries/netMHCcons/netMHCcons-1.1/netMHCcons'),
            Argument("ALLELE_LIST", 'list of alleles', default=''),
            Argument('PEPCSV', 'Table with ids', default=''),
            Argument('PEPCSVERROR', 'Table links FDR with prob', default=''),
        ]


    def prepare_run(self, log, info):
        print "Wenguang: sample: {}".format(info)
        workdir = info[Keys.WORKDIR]
        iprophoutput = info['PEPCSV']
        error_table = info['PEPCSVERROR']
        alleles = pso.fixallele(info['ALLELE_LIST'])
        print "Wenguang: allele: {}".format(alleles)
        #alleles = info['ALLELE_LIST']


        exe = info['NETMHCCONS']

        errorTable = pd.read_csv(error_table,sep="\t", header=0)
        prob_cut = errorTable[errorTable['error'] == 0.01]['min_prob'].mean()
        print "prob when FDR 0.01: {}".format(prob_cut)

        self.df = pd.read_csv(iprophoutput,sep="\t", header=0)
        self.df = self.df[self.df['iprophet_probability'] > prob_cut]
        uniqueSeq = self.df.drop_duplicates( subset=['search_hit'] )
        pepseq = uniqueSeq['search_hit'].tolist()

        self.outfiles, commands = pso.prepare_for_NetMhcCons(workdir, pepseq, alleles, exe)
        return info, commands


    def validate_run(self, log, info, exit_code, stdout):
        check_exitcode(log,exit_code)

        respiv = pso.concat_all_MHC_outputs_wshao(self.outfiles, self.df)

        info['NETMHC_OUT'] = os.path.join(info[Keys.WORKDIR], 'netmhccons.output.tsvh')
        respiv.to_csv(info ['NETMHC_OUT'], sep="\t")

        subprocess.call(["Rscript", "/home/systemhc/prog/systemhccake/systemhccake/process.r", "--args", info['NETMHC_OUT'], info["JOB_ID"]])

        peptide_table = pd.read_csv(os.path.join(info[Keys.WORKDIR], 'final.tsv'), sep="\t")


        imageloc = os.path.join(info[Keys.WORKDIR], 'heatmap.png')
        #self.plot_heatmap(respiv, imageloc)
        self.plot_heatmap(peptide_table, imageloc)



        #print'ssss: {}'.format(info)



        # get all the generated outptuts
        return info

    def plot_heatmap(self, respiv, imageloc, weak = 1000):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        #colnams = respiv.columns[0:-2].tolist()
        #toplot = respiv.ix[:, 0:-2]
        colnams = respiv.columns[3:-7].tolist()
        toplot = respiv.ix[:, 3:-7]
        toplot[toplot > weak] = weak
        toplot = toplot.sort_values(toplot.columns.tolist())

        fig, ax = plt.subplots()
        heatmap = ax.pcolor(toplot)
        ax.set_xticks(np.arange(toplot.shape[1]) + 0.5, minor=False)
        # ax.xaxis.tick_top()
        ax.set_xticklabels(colnams, minor=False)
        plt.colorbar(heatmap)
        plt.savefig(imageloc)
        plt.close()
        #return respiv





if __name__ == "__main__":
    sys.argv = ['--INPUT', '/home/systemhc/prog/systemhccake/systemhccake/convert2csv.ini', '--OUTPUT', 'test.ini']
    NetMHC.main()
