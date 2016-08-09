from applicake.base.app import WrappedApp
from applicake.base.coreutils.arguments import Argument
from applicake.base.coreutils.keys import Keys, KeyHelp
import pandas as pd
from applicake.base.apputils.validation import check_exitcode
import parseSearchOutput as pso
import os
import sys
import re
import getAlleleLists as gal

# ! /usr/bin/env python

def generateWeblogoCommands(exe, file, outfile ):
    command = "{exe} -F png < {file} > {outfile}".format(exe = exe, file=file, outfile=outfile)
    return command


def runweblogo_on_files(exe, files):
    commands = []
    for file in files:
        outfile = file + ".png"
        commands.append(generateWeblogoCommands(exe, file, outfile))
    return commands



def fixStupidGibbsclusterFile(fileinput, outfilename):
    pattern = re.compile("^Seq[0-9]+ ")
    outfile = 0
    outfiles = []
    with open(fileinput) as f:
        for line in f:
            if "## Sequence alignment for group" in line:
                print line
                groupid = line.replace("## Sequence alignment for group ", "")
                groupid = int(groupid)
                filename = outfilename + str(groupid) + ".motifin"
                outfiles.append(filename)
                print "group : " + str(groupid) + filename
                outfile = open(filename,"w")

            if pattern.match(line):
                elems = re.split(" +|\t", line);
                outfile.write(elems[1] + "\n")
    outfile.close()
    return(outfiles)


def prepare_for_Gibscluster(exe, workdir, pepseq, lengths=[8, 9, 10, 11]):
    commands = []
    outfiles = []

    fck = pso.maketxtfile(workdir, 'gibbs_in', 'pep', 'All')
    pso.mywrite(fck, pepseq)

    for length in lengths:
        outfile = pso.maketxtfile(workdir, 'gibbs_out', 'gibbs', length)
        command = "{exe} -fast -l {length} -s -1 {infile} > {outfile}".format(exe=exe,
                                                                              length=length,
                                                                              infile=fck,
                                                                              outfile=outfile)

        outfiles.append(outfile)
        commands.append(command)
    return outfiles, commands


class GibbsCluster(WrappedApp):
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
            Argument('PEPCSV', 'Table with ids', default=''),
        ]

    def prepare_run(self, log, info):
        sysmhcdir = os.environ.get('SYSTEMHC')

        if sysmhcdir is None:
            log.warning("systmhc not set")
        else:
            log.info('systemhc directory is: ' + sysmhcdir)

        workdir = info[Keys.WORKDIR]
        iprophoutput = info['PEPCSV']

        exe = info['GIBSCLUSTER']

        self.df = pd.read_csv(iprophoutput, sep="\t", header=0)
        uniqueSeq = self.df.drop_duplicates(subset=['search_hit'])
        pepseq = uniqueSeq['search_hit'].tolist()

        self.outfiles, commands = prepare_for_Gibscluster(exe, workdir, pepseq)

        return info, commands

    def validate_run(self, log, info, exit_code, stdout):
        check_exitcode(log, exit_code)

        weblogoexe = info['WEBLOGO']

        weblogoinputs = []
        for file in self.outfiles:
            weblogoinputs += fixStupidGibbsclusterFile(file, file + "out")

        commands = runweblogo_on_files(weblogoexe, weblogoinputs)
        self.execute_run(log, info, commands)

        # respiv = pso.concat_all_Gibbs_outputs(self.outfiles, self.df)
        # imageloc = os.path.join(info[Keys.WORKDIR], 'heatmap.png')
        # self.plot_heatmap(respiv, imageloc)

        #info['GIBBS_OUT'] = os.path.join(info[Keys.WORKDIR], 'netmhccons.output.csv')

        # get all the generated outputs
        return info


if __name__ == "__main__":
    sys.argv = ['--PEPCSV','/home/systemhc/prog/systemhccake/tests/PBMC1_Tub_short.csv']
    GibbsCluster.main()
