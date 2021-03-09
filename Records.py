# records and trends
import pandas as pd
from datetime import timezone
from datetime import datetime
import datetime
import time


def Records_trends (dfSQLall):
    print (dfSQLall.iloc[1,0])
    #Start_date = pd.Timestamp.date(dfSQLall.iloc[1,0])
    Start_date = dfSQLall.iloc[1,0]

    Max_Temp = max(dfSQLall['Outdoor_Temperature'])
    MaxTemp_Datetime = dfSQLall.query('Outdoor_Temperature == @Max_Temp').OurWeather_DateTime
    if dfSQLall.OurWeather_DateTime.dtypes != 'O':
       MaxTemp_Date = pd.Timestamp.date(MaxTemp_Datetime.iloc[0])
    else:
       MaxTemp_Date = MaxTemp_Datetime.iloc[0]
    print (MaxTemp_Date)

    Max_HeatIndex = max(dfSQLall['HeatIndex'])
    MaxHI_Datetime = dfSQLall.query('HeatIndex == @Max_HeatIndex').OurWeather_DateTime
    if dfSQLall.OurWeather_DateTime.dtypes != 'O':
       MaxHI_Date = pd.Timestamp.date(MaxHI_Datetime.iloc[0])
    else:
       MaxHI_Date = MaxHI_Datetime.iloc[0]
    print (MaxHI_Date)

    Min_Temp = min(dfSQLall['Outdoor_Temperature'])
    MinTemp_Datetime = dfSQLall.query('Outdoor_Temperature == @Min_Temp').OurWeather_DateTime
    if dfSQLall.OurWeather_DateTime.dtypes != 'O':
           MinTemp_Date = pd.Timestamp.date(MinTemp_Datetime.iloc[0])
    else:
           MinTemp_Date = MinTemp_Datetime.iloc[0]
    print (MinTemp_Date)

    Min_WindChill = min(dfSQLall['WindChill'])
    MinWC_Datetime = dfSQLall.query('WindChill == @Min_WindChill').OurWeather_DateTime
    if dfSQLall.OurWeather_DateTime.dtypes != 'O':
           MinWC_Date = pd.Timestamp.date(MinWC_Datetime.iloc[0])
    else:
           MinWC_Date = MinWC_Datetime.iloc[0]
    print (MinWC_Date)

    Max_BP = max(dfSQLall['Barometric_Pressure'])
    MaxBP_Datetime = dfSQLall.query('Barometric_Pressure == @Max_BP').OurWeather_DateTime
    if dfSQLall.OurWeather_DateTime.dtypes != 'O':
           MaxBP_Date = pd.Timestamp.date(MaxBP_Datetime.iloc[0])
    else: 
           MaxBP_Date = MaxBP_Datetime.iloc[0]
    print (MaxBP_Date)

    Min_BP = min(dfSQLall['Barometric_Pressure'])
    MinBP_Datetime = dfSQLall.query('Barometric_Pressure == @Min_BP').OurWeather_DateTime
    if dfSQLall.OurWeather_DateTime.dtypes != 'O':
           MinBP_Date = pd.Timestamp.date(MinBP_Datetime.iloc[0])
    else:
           MinBP_Date = MinBP_Datetime.iloc[0]
    print (MinBP_Date)

    Max_Wind_spd = max(dfSQLall['Current_Wind_Gust'])
    MaxWind_Datetime = dfSQLall.query('Current_Wind_Gust == @Max_Wind_spd').OurWeather_DateTime
    if dfSQLall.OurWeather_DateTime.dtypes != 'O':
           MaxWind_Date = pd.Timestamp.date(MaxWind_Datetime.iloc[0])
    else:
           MaxWind_Date = MaxWind_Datetime.iloc[0]
    print (MaxWind_Date)

    Max_Rain_Total = max(dfSQLall['Rain_Total'])
    MaxRain_Datetime = dfSQLall.query('Rain_Total == @Max_Rain_Total').OurWeather_DateTime
    if dfSQLall.OurWeather_DateTime.dtypes != 'O':
           MaxRain_Date = pd.Timestamp.date(MaxRain_Datetime.iloc[0])
    else:
           MaxRain_Date = MaxRain_Datetime.iloc[0]
    print (MaxRain_Date)


    Min_Rel_Humidity = min(dfSQLall['Outdoor_Humidity'])
    MinRelHum_Datetime = dfSQLall.query('Outdoor_Humidity == @Min_Rel_Humidity').OurWeather_DateTime
    if dfSQLall.OurWeather_DateTime.dtypes != 'O':
           MinRelHum_Date = pd.Timestamp.date(MinRelHum_Datetime.iloc[0])
    else:
           MinRelHum_Date = MinRelHum_Datetime.iloc[0]
    print (MinRelHum_Date) 

    Overall_Avg_Temp = dfSQLall.mean(axis =0)['Outdoor_Temperature'] 
    Overall_Avg_Humidity = dfSQLall.mean(axis =0)['Outdoor_Humidity']
    Overall_Avg_BP = dfSQLall.mean(axis =0)['Barometric_Pressure']

    # build a routine to get average summer and winter temperatures for trends
    # build a routine for overall trends
          
    Records = {'Item':['Start_date', 'Max_Temp', 'Max_HeatIndex','Min_Temp',
                       'Min_WindChill','Max_BP','Min_BP','Max_Wind_spd','Max_Rain_Total',
        'Min_Rel_Humidity','Overall_Avg_Temp','Overall_Avg_Humidity','Overall_Avg_BP'],
               'Value':[Start_date, Max_Temp, Max_HeatIndex, Min_Temp, Min_WindChill, Max_BP, Min_BP, Max_Wind_spd, Max_Rain_Total,
        Min_Rel_Humidity, Overall_Avg_Temp, Overall_Avg_Humidity, Overall_Avg_BP],
                'Units': ['YYYY-MM-DD', 'degC', 'degC', 'degC', 'degC','Pa','Pa','kph','mm','rel%', 'degC', 'rel%', 'Pa'], 
               'Date Occured':['NA', MaxTemp_Date, MaxHI_Date, MinTemp_Date, MinWC_Date, MaxBP_Date, MinBP_Date, MaxWind_Date, MaxRain_Date,
        MinRelHum_Date, 'NA', 'NA', 'NA'],
               }
    
    DFRecords = pd.DataFrame(Records, columns=['Item','Value','Units','Date Occured',])

    return DFRecords