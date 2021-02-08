# records and trends
import pandas as pd
from datetime import timezone
from datetime import datetime
import datetime
#import time


def Records_trends (dfSQLall):
    Start_date = pd.Timestamp.date(dfSQLall.iloc[1,0])
    
    Max_Temp = max(dfSQLall['Outdoor_Temperature'])
    MaxTemp_Datetime = dfSQLall.query('Outdoor_Temperature == @Max_Temp').OurWeather_DateTime
    MaxTemp_Date = pd.Timestamp.date(MaxTemp_Datetime.iloc[0])
    
    Min_Temp = min(dfSQLall['Outdoor_Temperature'])
    MinTemp_Datetime = dfSQLall.query('Outdoor_Temperature == @Min_Temp').OurWeather_DateTime
    MinTemp_Date = pd.Timestamp.date(MinTemp_Datetime.iloc[0])

    Max_BP = max(dfSQLall['Barometric_Pressure'])
    MaxBP_Datetime = dfSQLall.query('Barometric_Pressure == @Max_BP').OurWeather_DateTime
    MaxBP_Date = pd.Timestamp.date(MaxBP_Datetime.iloc[0])

    Min_BP = min(dfSQLall['Barometric_Pressure'])
    MinBP_Datetime = dfSQLall.query('Barometric_Pressure == @Min_BP').OurWeather_DateTime
    MinBP_Date = pd.Timestamp.date(MinBP_Datetime.iloc[0])
    
    Max_Wind_spd = max(dfSQLall['Current_Wind_Gust'])
    MaxWind_Datetime = dfSQLall.query('Current_Wind_Gust == @Max_Wind_spd').OurWeather_DateTime
    MaxWind_Date = pd.Timestamp.date(MaxWind_Datetime.iloc[0])
    
    Max_Rain_Total = max(dfSQLall['Rain_Total'])
    MaxRain_Datetime = dfSQLall.query('Rain_Total == @Max_Rain_Total').OurWeather_DateTime
    MaxRain_Date = pd.Timestamp.date(MaxRain_Datetime.iloc[0])

    Min_Rel_Humidity = min(dfSQLall['Outdoor_Humidity'])
    MinRelHum_Datetime = dfSQLall.query('Outdoor_Humidity == @Min_Rel_Humidity').OurWeather_DateTime
    MinRelHum_Date = pd.Timestamp.date(MinRelHum_Datetime.iloc[0])

    Overall_Avg_Temp = dfSQLall.mean(axis =0)['Outdoor_Temperature'] 
    Overall_Avg_Humidity = dfSQLall.mean(axis =0)['Outdoor_Humidity']
    Overall_Avg_BP = dfSQLall.mean(axis =0)['Barometric_Pressure']

    # build a routine to get average summer and winter temperatures for trends
    # build a routine for overall trends
    # put the data with units into a dataframe
      
    Records = {'Item':['Start_date', 'Max_Temp','Min_Temp','Max_BP','Min_BP','Max_Wind_spd','Max_Rain_Total',
        'Min_Rel_Humidity','Overall_Avg_Temp','Overall_Avg_Humidity','Overall_Avg_BP'],
               'Value':[Start_date, Max_Temp, Min_Temp, Max_BP, Min_BP, Max_Wind_spd, Max_Rain_Total,
        Min_Rel_Humidity, Overall_Avg_Temp, Overall_Avg_Humidity, Overall_Avg_BP],
                'Units': ['YYYY-MM-DD', 'degC', 'degC','Pa','Pa','kph','mm','rel%', 'degC', 'rel%', 'Pa'], 
               'Date Occured':['NA', MaxTemp_Date, MinTemp_Date, MaxBP_Date, MinBP_Date, MaxWind_Date, MaxRain_Date,
        MinRelHum_Date, 'NA', 'NA', 'NA'],
               }
    
    DFRecords = pd.DataFrame(Records, columns=['Item','Value','Units','Date Occured',])

    return DFRecords