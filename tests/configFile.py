import os
import glob
from applicake2.base import get_handler
from applicake2.base.apputils import dicts



def setup_windows():
    return '''
TPPDIR=c:/users/wewol/prog/searchcake_binaries/tpp/windows/windows_64bit/
'''

def spectrastParams():
    return '''
#Spectrast parameters
MS_TYPE=CID-QTOF
CONSENSUS_TYPE=consensus
DECOY=DECOY_
IPROB=0.1
'''

def netMHCParams():
    return '''
ALLELE_LIST=
'''

def setup_linux():
    return '''
TPPDIR={systemhc}/searchcake_binaries/tpp/ubuntu14.04/bin/
SPECTRASTDIR={systemhc}/SysteMHC_Binaries/spectraST/
'''.format(systemhc=os.environ.get('SYSTEMHC'))


def setup_general():
    return """
LOG_LEVEL = DEBUG
COMMENT = bbWFTEST - newUPS TPP
"""

def setup_netMHC():
    return '''
MZXML =
THREADS = 4
LOG_LEVEL = DEBUG
DBASE =
TPPDIR = {systemhc}/searchcake_binaries/tpp/ubuntu14.04/bin/
SPECTRASTDIR = {systemhc}/SysteMHC_Binaries/spectraST/
ALLELE_LIST = B39:01, C07:01
COMMENT = bbWFTEST - newUPS TPP
BASEDIR = .
MODULE = ""
STATIC_MODS = ""
DECOY = DECOY_
MISSEDCLEAVAGE = 0
PEPXML =
FDR_TYPE = iprophet-pepFDR
    '''.format(systemhc=os.environ.get('SYSTEMHC'))

def setup_search(massspec):
    if massspec in {'Triple-TOF 5600', 'Q-Exactive', 'Q-Exactive Plus', 'Q-Exactive HF', 'Orbitrap Fusion'}:
        return '''
 # Search parameters
FDR_TYPE = iprophet-pepFDR
FRAGMASSERR = 0.05
FRAGMASSUNIT = Da
PRECMASSERR = 15
PRECMASSUNIT = ppm
MISSEDCLEAVAGE = 0
ENZYME = Nonspecific
STATIC_MODS =
VARIABLE_MODS = Oxidation (M)
comet_fragment_bin_offset = 0.0
comet_theoretical_fragment_ions = 0

## TPP
DECOY = DECOY_
IPROPHET_ARGS = MINPROB=0
MZXML =
DBASE =
    '''
    else:
        return '''
 # Search parameters
FDR_TYPE = iprophet-pepFDR
FRAGMASSERR = 0.5
FRAGMASSUNIT = Da
PRECMASSERR = 15
PRECMASSUNIT = ppm
MISSEDCLEAVAGE = 0
ENZYME = Nonspecific
STATIC_MODS =
VARIABLE_MODS = Oxidation (M)
comet_fragment_bin_offset = 0.4
comet_theoretical_fragment_ions = 1

## TPP
DECOY = DECOY_
IPROPHET_ARGS = MINPROB=0
MZXML =
DBASE =
    '''


def getTuberculosisData():
    return ['carone_20150801_QEp7_MiBa_SA_iRT_BCG_1.mzXML',
            'carone_20150801_QEp7_MiBa_SA_iRT_BCG_2.mzXML',
            'carone_20150801_QEp7_MiBa_SA_iRT_THP_1.mzXML',
            'carone_20150801_QEp7_MiBa_SA_iRT_THP_2.mzXML',
            'carone_Y150824_001_THP1_DDA.mzXML',
            'carone_Y150824_001_THP1_rBCG_DDA.mzXML'
            ]

def getMZXMLTub1():
    return ['PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep1_msms1_c.mzXML',
            'PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep2_msms2_c.mzXML',
            'PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep3_msms3_c.mzXML',
            'PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep4_msms4_c.mzXML',
            'PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep5_msms5_c.mzXML']

def getMZXMLTub2PBMC10():
    return ['PBMC10_Tubingen_130429_SKUG_Buffy83_W_1p25ug_20_50umx15cmColumn_60min3sDynExcl_3_msms4_c.mzXML',
            'PBMC10_Tubingen_130430_SKUG_Buffy83_W_1p25ug_20_15cm60min3sDynExcl_4_msms27_c.mzXML']

def getMZXMLTub3():
    return ['PBMC11_Tubingen_130510_SKUG_Buffy85_W_2p00ug_20_Rep_1_msms6_c.mzXML',
            'PBMC11_Tubingen_130510_SKUG_Buffy85_W_2p00ug_20_Rep_2_msms7_c.mzXML',
            'PBMC11_Tubingen_130510_SKUG_Buffy85_W_2p00ug_20_Rep_3_msms8_c.mzXML',
            'PBMC11_Tubingen_130510_SKUG_Buffy85_W_2p00ug_20_Rep_4_msms9_c.mzXML',
            'PBMC11_Tubingen_130510_SKUG_Buffy85_W_2p00ug_20_Rep_5_msms10_c.mzXML']


def getDB(organism):
    if(organism == "Human"):
        return '{systemhc}/SysteMHC_Data/fasta/CNCL_05640_2015_09_DECOY.fasta'.format(systemhc=os.environ.get('SYSTEMHC'))
    elif(organism == "Mycobacterium tuberculosis"):
        return '{systemhc}/SysteMHC_Data/fasta/carone_hsp_MtbII_DECOY_141017.fasta'.format(systemhc=os.environ.get('SYSTEMHC'))
    else:
        return '{systemhc}/SysteMHC_Data/fasta/mtb_plus_human_DECOY.fasta'.format(systemhc=os.environ.get('SYSTEMHC'))


def getTubercoDB():
    return '{systemhc}/SysteMHC_Data/fasta/mycBovis.fasta'.format(systemhc=os.environ.get('SYSTEMHC'))


def getHumanTubercoDB():
    return '{systemhc}/SysteMHC_Data/fasta/Mycobacterium_bovis_BCG_str_ATCC_35733_PATRIC_decoy_uniprot_20209_reviewed_canonical_irt_reverse_140724.fasta'.format(systemhc=os.environ.get('SYSTEMHC'))


def write_ini(ini, filename="input.ini", dest="."):
    with open(os.path.join(dest, filename), 'w+') as f:
        f.write(ini)



def remove_ini_log():
    for fl in glob.glob("*.ini*"):
        os.remove(fl)
    for fl in glob.glob("*.log*"):
        os.remove(fl)


def peptidesearch_overwriteInfo(overwrite, filename="input.ini"):
    inifile = overwrite['INPUT']
    ih = get_handler(inifile)
    fileinfo = ih.read(inifile)
    info = dicts.merge(overwrite, fileinfo)
    ih.write(info,filename)
    return info

def getMzXMLFiles(path,extension="mzXML"):
    import glob
    dd = path + "*." + extension
    print (dd)
    return glob.glob(dd)

def getMzXMLFiles(path,extension="mzXML"):
    import glob
    dd = path + "*." + extension
    print (dd)
    return glob.glob(dd)
