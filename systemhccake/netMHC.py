from applicake.base.app import WrappedApp
from applicake.base.apputils import validation
from applicake.base.coreutils.arguments import Argument
from applicake.base.coreutils.keys import Keys, KeyHelp
import pandas as pd

import os

panAlleles = '/home/witold/prog/SysteMHC_Binaries/netMHCpan/netMHCpan-2.8/data/MHC_pseudo.dat'
panAlleles = pd.read_csv(panAlleles)

netMHCalleles='/home/witold/prog/SysteMHC_Binaries/netMHC/netMHC-3.4/etc/net'
netMHCalleles = os.listdir(netMHCalleles)


class NetMHC(WrappedApp):
    def add_args(self):
        return [
            Argument("NETMHCDIR",  KeyHelp.EXECDIR, default=''),
            Argument("ALLELE_LIST", 'list of alleles', default='InterProphetParser'),
            Argument(Keys.WORKDIR, KeyHelp.WORKDIR),
            Argument('IPROPHETOUTPUT', 'Arguments for InterProphetParser', default='MINPROB=0'),
        ]

    def prepare_run(self, log, info):
        pass
        #create commands


    def validate_run(self, log, info, exit_code, stdout):
        pass
        # get all the generated outptuts


if __name__ == "__main__":
    NetMHC.main()
