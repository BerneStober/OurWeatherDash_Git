import os
from datetime import datetime
import time
# change below to the location of your code 
os.chdir(r'C:\Users\berny\source\repos\OurWeatherDash')
import Dash_functions2
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

# this code grabs data every 1.5 minute for a day
# it is run with windows scheduler every day 
counter = 0
MaxCounter = 959
SecBetweenDataGrab = 90
# this below is set so that any delays in the data grab don't cause overall problems.
MaxElapsedTime = 86000
t0= time.time()

while (counter <= MaxCounter) or (ElapsedTime < MaxElapsedTime): 

    df = Dash_functions2.readOURWEATHERData(UnitDisplay, OldUnit, Unit_toggle)
    df.to_pickle('Stored_ourweather_dataframe.pkl')
    #WriteDebug ('df: \n', df, '\n')
    print('df: \n', df, '\n')
    counter = counter + 1
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    WriteDebug (dt_string + ' at execution number' + str(counter) + ' now pausing for another ' + str(SecBetweenDataGrab) + ' seconds.')
    print (dt_string + ' at execution number' + str(counter) + ' now pausing for another ' + str(SecBetweenDataGrab) + ' seconds.')
    Pausing (SecBetweenDataGrab)
    ElapsedTime = time.time() - t0
    WriteDebug (dt_string + ' at execution number' + str(counter) + ' ' + str(ElapsedTime) + ' seconds.')
    print (dt_string + ' at execution number' + str(counter) + ' ' + str(ElapsedTime) + ' seconds.')

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print ('Execution completed at '+ dt_string)

