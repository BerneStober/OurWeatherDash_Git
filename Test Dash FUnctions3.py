import os
import sys
os.chdir(r'C:\Users\YYYYY\source\repos\OurWeatherDashV3')
import Dash_functions3
import pandas as pd
import Records
import datetime
import time
from dateutil.parser import parse

import plotly.express as px
f = sys.stdout
pd.set_option("display.max_rows", 20, "display.max_columns", 10)
pd.set_option('display.width', 180)
#unit = [{'OurWeather_DateTime':'Units', 'Outdoor_Temperature':'degC', 'Outdoor_Humidity':'rel%', 'Barometric_Pressure':'Pa', 'Current_Wind_Speed':'kph', 'Current_Wind_Gust':'kph', 'Current_Wind_Direction':'deg', 'Rain_Total':'mm', 'Current_Air_Quality_Sensor':'NA', 'Current_Air_Quality_Qualitative':'NA', 'id':'NA'}]
#df = pd.DataFrame(unit)
UnitDisplay = 'metric'
OldUnit = 'English'
Unit_toggle=0
#df = Dash_functions2.readOURWEATHERData(UnitDisplay, OldUnit, Unit_toggle)
#df, dfSQLall = Dash_functions2.GetSQLData(0)
#dfdisplay_all, dfSQLall = Dash_functions3.GetSQLData(0)
df = pd.read_pickle('Stored_ourweather_dataframe.pkl')
print(df)

HI_row = {'Value':Dash_functions3.HeatIndex(df), 'Units':'degC', 'Measurement':'Calculated HeatIndex'}
WC_row = {'Value':Dash_functions3.WindChill(df), 'Units':'degC', 'Measurement':'Calculated WindChill'}
HI_row_df = pd.DataFrame([HI_row], index = ['HeatIndex'])
WC_row_df = pd.DataFrame([WC_row], index = ['WindChill'])
df = pd.concat([df,HI_row_df,WC_row_df])
df = df.reindex(['OurWeatherTime','OutdoorTemperature','HeatIndex','WindChill','OutdoorHumidity','BarometricPressure','WindSpeedMax','CurrentWindGust','CurrentWindDirection','WindDirectionMin','WindDirectionMax','WindGustMax','WindGustMin','AirQualitySensor','Altitude','IndoorTemperature','RainTotal'])


print (df)


#DFRecords = Records.Records_trends(dfSQLall)
#print (DFRecords)
#Dash_functions3.AddHeatIndexWindChill (dfSQLall)
#dfSQLall['HeatIndex'] = dfSQLall.apply(HeatIndex, axis =1)

#MinDate = dfSQLall.head(1)['OurWeather_DateTime'].dt.date
#MaxDate = dfSQLall.tail(1)['OurWeather_DateTime'].dt.date`
#MinDate = pd.Timestamp.date(dfSQLall.iloc[1,0])
#MinDate = dfSQLall.iloc[1,0]
#row_count =  dfSQLall.shape[0]
#MinDate = min(dfSQLall['OurWeather_DateTime'].dt.date)
#MaxDate = dfSQLall.iloc[row_count-1,0]
#print (MinDate, MaxDate)
#Min = datetime.datetime.strptime(MinDate, '%Y-%m-%d %H:%M:%S')
#Max = datetime.datetime.strptime(MaxDate, '%Y-%m-%d %H:%M:%S')
#DateSection = (Max - Min)/8
"""
if dfSQLall.OurWeather_DateTime.dtypes == 'O':
    MinDate1 = dfSQLall.iloc[1,0]
    row_count =  dfSQLall.shape[0]
    MaxDate1 = dfSQLall.iloc[row_count-1,0]
    print (MinDate1, MaxDate1, file=f)
    #MinDate = datetime.datetime.strptime(MinDate1, '%Y-%m-%d %H:%M:%S')
    MinDate = parse(MinDate1).date()
    #MaxDate = datetime.datetime.strptime(MaxDate, '%Y-%m-%d %H:%M:%S')
    MaxDate = parse(MaxDate1).date()
    print (MinDate, MaxDate, file=f)

else: 
    print ('Assuming OurWeather_DateTime is a DateTime',file=f)
    MinDate = pd.Timestamp.date(dfSQLall.iloc[1,0])
    MaxDate = max(dfSQLall['OurWeather_DateTime'].dt.date)



DateSection = (MaxDate - MinDate)/8
print ('DateSection : ',DateSection, file=f)


print (DateSection)

# not sure if this needed, dummy dates to define it
dates = ['2015-02-17', '2015-05-17', '2015-08-17', '2015-11-17',
         '2016-02-17', '2016-05-17', '2016-08-17', '2016-11-17', '2017-02-17']


i = 0
while i < 9:
    dates[i] = MinDate + i * DateSection
    i += 1 

print('Enter lower index: lt 8')
X1 = input()

print('Enter higher index index: gt lower lt 8')
X2 = input()
X1 = int(X1)
X2 = int(X2)



print('Lower index: ', X1)
print('Higher index: ', X2)

dfSQLall['OurWeather_DateTime'] = pd.to_datetime(dfSQLall['OurWeather_DateTime'], infer_datetime_format=True).dt.date

dfSQLall2 = dfSQLall[(dfSQLall.OurWeather_DateTime > dates[X1]) & (dfSQLall.OurWeather_DateTime < dates[X2])]

"""
#figOutdoor_Temperature = px.line(dfSQLall, x='OurWeather_DateTime', y='Outdoor_Temperature', title='Outdoor Temperature Time Series')
#figOutdoor_Temperature.show()

#figBarometric_Pressure = px.line(dfSQLall, x='OurWeather_DateTime', y='Barometric_Pressure', title='Barometric Pressure Time Series')
#figBarometric_Pressure.show()

#print('dfdisplay: \n', dfdisplay, '\n')

#print('dfSQL: \n', dfSQL, '\n')

#dfSQLall.to_pickle('Stored_ourweather_SQL_all_dataframe.pkl') 
#dfSQLall = pd.read_pickle('Stored_ourweather_SQL_all_dataframe.pkl

#DFRecords = Records.Records_trends(dfSQLall)

#print (DFRecords, '\n')

#df = df[['Measurement','Value','Units']]
