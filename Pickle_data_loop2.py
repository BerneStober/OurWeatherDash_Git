import os
from datetime import datetime
import time
os.chdir(r'C:\Users\YYYYY\source\repos\OurWeatherDashV3')
import Dash_functions3
import pandas as pd

pd.set_option("display.max_rows", 20, "display.max_columns", 10)
pd.set_option('display.width', 180)

UnitDisplay = 'metric'
OldUnit = 'English'
Unit_toggle=0

def WriteDebug (record):
    debugfile = open("PickleDataLoopdebug.txt",'a+t')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    debugfile.write(dt_string + ' ' + record + "\n")
    debugfile.close()

def Pausing (sec):
    time.sleep(sec)

counter = 0
MaxCounter = 39
SecBetweenDataGrab = 90
MaxElapsedTime = 3590
t0= time.time()

while (counter <= MaxCounter) or (ElapsedTime < MaxElapsedTime): 

    df = Dash_functions3.readOURWEATHERData(UnitDisplay, OldUnit, Unit_toggle)
    df.to_pickle('Stored_ourweather_dataframe_V2.pkl')
    #WriteDebug ('df: \n', df, '\n')
    #print('Pickle 2 df: \n', df, '\n')
    counter = counter + 1
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    WriteDebug (dt_string + ' at execution number' + str(counter) + ' now pausing for another ' + str(SecBetweenDataGrab) + ' seconds.')
    #print ('Pickle 2 ' + dt_string + ' at execution number' + str(counter) + ' now pausing for another ' + str(SecBetweenDataGrab) + ' seconds.')
    Pausing (SecBetweenDataGrab)
    ElapsedTime = time.time() - t0
    WriteDebug (dt_string + ' at execution number' + str(counter) + ' ' + str(ElapsedTime) + ' seconds.')
    #print (dt_string + ' at execution number' + str(counter) + ' ' + str(ElapsedTime) + ' seconds.')

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print ('Pickle 2 Execution completed at '+ dt_string)

