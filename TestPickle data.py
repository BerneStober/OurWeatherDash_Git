import os
os.chdir(r'C:\Users\YYYYY\source\repos\OurWeatherDash')
import Dash_functions3
import pandas as pd
import Records
pd.set_option("display.max_rows", 27, "display.max_columns", 10)
pd.set_option('display.width', 180)

UnitDisplay = 'metric'
OldUnit = 'English'
Unit_toggle=0


dfV1 = pd.read_pickle('Stored_ourweather_dataframe_V1.pkl')
dfV2 = Dash_functions3.readOURWEATHERData(UnitDisplay, OldUnit, Unit_toggle)
    
dfV2.to_pickle('Stored_ourweather_dataframe_V2.pkl')

print('dfV1: \n', dfV1, '\n')
print('dfV2: \n', dfV2, '\n')