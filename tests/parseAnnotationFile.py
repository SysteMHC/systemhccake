import pandas as pd
import os



path = "{}/SysteMHC_Data/annotation/cleanedTable_id.csv".format(
    os.environ.get('SYSTEMHC'))
df = pd.read_csv(path)


path = "/mnt/Systemhc/Data/process/1606192042/IprohetPepXML2CSV/"



