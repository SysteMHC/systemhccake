#!/usr/bin/env python
import sys

# identification workflow for systeMHC

from ruffus import *
from applicake2.apps.flow.jobid import Jobid

from searchcake.searchengines.iprophetpepxml2csv import IprohetPepXML2CSV
from searchcake.libcreate.spectrast import Spectrast

from multiprocessing import freeze_support
from systemhccake.netMHC import NetMHC


@files("inputX.ini", "jobidX.ini")
def jobid(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    Jobid.main()

########################## MERGE ALL DATASETS ######################
@follows(jobid)
@files("jobidX.ini", "convert2csv.ini")
def convert2csv(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    IprohetPepXML2CSV.main()

####################### Spectrast ###################################
@follows(convert2csv)
@files("jobidX.ini", "spectrast.ini")
def pepxml2spectrast(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    Spectrast.main()

################################ NETMHC #############################
@follows(pepxml2spectrast)
@files("convert2csv.ini", "netMHC.ini")
def runNetMHC(infile, outfile):
    sys.argv = ['--INPUT', infile, "--OUTPUT", outfile]
    NetMHC.main()


def run_libcreate_withNetMHC_WF(nrthreads=3):
    freeze_support()
    pipeline_run([runNetMHC], multiprocess=nrthreads)
