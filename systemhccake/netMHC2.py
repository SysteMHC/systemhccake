from applicake.base.app import WrappedApp
from applicake.base.coreutils.arguments import Argument
from applicake.base.coreutils.keys import Keys, KeyHelp
import pandas as pd
from applicake.base.apputils.validation import check_exitcode
import parseSearchOutput as pso
import os
import sys

class NetMHC2(WrappedApp):
    outfiles = []

    def add_args(self):
        return [
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument("NETMHCCONS",
                     KeyHelp.EXECDIR,
                     default='{}/SysteMHC_Binaries/netMHCcons/netMHCcons-1.1/netMHCcons'.format(
                         os.environ.get('SYSTEMHC'))),
            Argument("DB_PATH", 'path to file with allele mzXML file mapings', default=''),
            Argument('PEPCSV', 'Table with ids', default=''),
        ]

    def prepare_run(self, log, info):
        workdir = info[Keys.WORKDIR]
        iprophoutput = info['PEPCSV']

        exe = info['NETMHCCONS']
        dbpath = info['DB_PATH']
        self.db = pd.read_csv(dbpath, sep=",", header=0)
        self.iprophet = pd.read_csv(iprophoutput, sep="\t", header=0)

        filesiprophet = list(self.iprophet['spectrum'])
        filesiprophet = map(lambda w: w.split(".")[0], filesiprophet)
        self.iprophet['fileid'] = filesiprophet

        filesdb = list(self.db['FileName'])
        filesdb = map(lambda w: os.path.splitext(w)[0], filesdb)
        self.db['fileid'] = filesdb

        self.mergefiles = self.iprophet.merge(self.db, left_on='fileid', right_on='fileid', how='inner')

        sampleIDs = self.mergefiles['SampleID'].unique()

        self.outfiles = []
        self.commands = []

        for sampleID in sampleIDs:
            allSet = self.mergefiles[self.mergefiles['SampleID'] == sampleID]
            alleles = (allSet['MHCAllele'].unique()).tolist()
            if (len(alleles) != 1):
                log.warning("there is more than one allele : {}".format('-'.join(alleles)))
            pepseq = (allSet['search_hit'].unique()).tolist()
            alleles = alleles[0].split(',')
            tmpdir = os.path.join(workdir, sampleID)
            if not os.path.exists(tmpdir):
                os.makedirs(tmpdir)
            print tmpdir
            outfiles, commands = pso.prepare_for_NetMhcCons(tmpdir, pepseq, alleles, exe)
            self.outfiles += outfiles
            self.commands += commands
        return info, self.commands


    def validate_run(self, log, info, exit_code, stdout):
        check_exitcode(log, exit_code)

        folders = map(os.path.dirname, self.outfiles)
        ufold = list(set(folders))
        info['NETMHC_OUT'] = []
        for fold in ufold:
            files = [x for x in self.outfiles if os.path.dirname(x) in fold]
            respiv = pso.concat_all_MHC_outputs(files, self.iprophet)
            outfile = os.path.join(fold, 'netmhccons.output.csv')
            respiv.to_csv(outfile, sep="\t")
            info['NETMHC_OUT'] += outfile
        return info


if __name__ == "__main__":
    db_path = "{}/SysteMHC_Data/annotation/cleanedTable_id.csv".format(
        os.environ.get('SYSTEMHC'))
    sys.argv = ['--PEPCSV', '/mnt/Systemhc/Data/process/1606192042/IprohetPepXML2CSV/ipeptide.csv', '--DB_PATH',
                db_path]
    NetMHC2.main()
