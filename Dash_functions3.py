from sqlalchemy import create_engine
import pymysql
import pandas as pd
import httplib2 as http
import json
import sys
from datetime import timezone
#from datetime import datetime
import datetime
import MySQLdb as mdb
import os
import urllib
from urllib import request
pd.set_option("display.max_rows", 20, "display.max_columns", 8)
pd.set_option('display.width', 100)

def getResponse(uri):
    operUrl = urllib.request.urlopen(uri)
    if(operUrl.getcode()==200):
        data = operUrl.read()
        
    else:
        print("Error receiving data", operUrl.getcode())
    return data

def ConvertUnits(UnitDisplay, OldUnit, values):
    English_len = lambda x: 3.28*x
    English_len_unit = lambda x: 'ft' if x == 'm' else x
    English_pres = lambda x: x/3386.75
    English_pres_unit = lambda x: 'inHg' if x == 'Pa' else x
    English_spd = lambda x: 0.62137*x
    English_spd_unit = lambda x: 'mph' if x == 'kph' else x
    English_tmp = lambda x: (9/5*x + 32)
    English_tmp_unit = lambda x: 'degF' if x == 'degC' else x
    English_hght = lambda x: x/25.4
    English_hght_unit = lambda x: 'in' if x == 'mm' else x
    
    metric_len = lambda x: x/3.28
    metric_len_unit = lambda x: 'm' if x == 'ft' else x
    metric_pres = lambda x: x*3386.75
    metric_pres_unit = lambda x: 'Pa' if x == 'inHg' else x
    metric_spd = lambda x: x/0.62137
    metric_spd_unit = lambda x: 'kph' if x == 'mph' else x
    metric_tmp = lambda x: (x - 32)*5/9
    metric_tmp_unit = lambda x: 'degC' if x == 'degF' else x
    metric_hght = lambda x: x*25.4
    metric_hght_unit = lambda x: 'mm' if x == 'in' else x
    
    if UnitDisplay == 'English' and OldUnit == 'metric':
        values['Value'] = values.apply(lambda x: English_len(x['Value']) if x['Units'] == 'm' else x['Value'], axis=1)
        values['Units'] = values.apply(lambda x: English_len_unit(x['Units']), axis=1)
        
        values['Value'] = values.apply(lambda x: English_pres(x['Value']) if x['Units'] == 'Pa' else x['Value'], axis=1)
        values['Units'] = values.apply(lambda x: English_pres_unit(x['Units']), axis=1)
        
        values['Value'] = values.apply(lambda x: English_spd(x['Value']) if x['Units'] == 'kph' else x['Value'], axis=1)
        values['Units'] = values.apply(lambda x: English_spd_unit(x['Units']), axis=1)

        values['Value'] = values.apply(lambda x: English_tmp(x['Value']) if x['Units'] == 'degC' else x['Value'], axis=1)
        values['Units'] = values.apply(lambda x: English_tmp_unit(x['Units']), axis=1)

        values['Value'] = values.apply(lambda x: English_hght(x['Value']) if x['Units'] == 'mm' else x['Value'], axis=1)
        values['Units'] = values.apply(lambda x: English_hght_unit(x['Units']), axis=1)

    elif UnitDisplay == 'metric' and OldUnit == 'English': 
        values['Value'] = values.apply(lambda x: metric_len(x['Value']) if x['Units'] == 'ft' else x['Value'], axis=1)
        values['Units'] = values.apply(lambda x: metric_len_unit(x['Units']), axis=1) 
        
        values['Value'] = values.apply(lambda x: metric_pres(x['Value']) if x['Units'] == 'inHg' else x['Value'], axis=1)
        values['Units'] = values.apply(lambda x: metric_pres_unit(x['Units']), axis=1)     
        
        values['Value'] = values.apply(lambda x: metric_spd(x['Value']) if x['Units'] == 'mph' else x['Value'], axis=1)
        values['Units'] = values.apply(lambda x: metric_spd_unit(x['Units']), axis=1)  
        
        values['Value'] = values.apply(lambda x: metric_tmp(x['Value']) if x['Units'] ==  'degF' else x['Value'], axis=1)
        values['Units'] = values.apply(lambda x: metric_tmp_unit(x['Units']), axis=1)   

        values['Value'] = values.apply(lambda x: metric_hght(x['Value']) if x['Units'] ==  'in' else x['Value'], axis=1)
        values['Units'] = values.apply(lambda x: metric_hght_unit(x['Units']), axis=1)   

def ConvertUnitsCols(UnitDisplay, OldUnit, values):
    
    English_len = lambda x: 3.28*x
    English_pres = lambda x: x/3386.75
    English_spd = lambda x: 0.62137*x
    English_tmp = lambda x: (9/5*x + 32)
    English_hght = lambda x: x/25.4
    
    
    metric_len = lambda x: x/3.28
    metric_pres = lambda x: x*3386.75
    metric_spd = lambda x: x/0.62137
    metric_tmp = lambda x: (x - 32)*5/9
    metric_hght = lambda x: x*25.4
        
    if UnitDisplay == 'English' and OldUnit == 'metric':

        values['Barometric_Pressure'] = values.apply(lambda x: English_pres(x['Barometric_Pressure']), axis=1)
                
        values['Current_Wind_Speed'] = values.apply(lambda x: English_spd(x['Current_Wind_Speed']), axis=1)
        
        values['Current_Wind_Gust'] = values.apply(lambda x: English_spd(x['Current_Wind_Gust']), axis=1)
        
        values['Outdoor_Temperature'] = values.apply(lambda x: English_tmp(x['Outdoor_Temperature']), axis=1)
        
        values['Rain_Total'] = values.apply(lambda x: English_hght(x['Rain_Total']), axis=1)
   
    elif UnitDisplay == 'metric' and OldUnit == 'English': 
        
        values['Barometric_Pressure'] = values.apply(lambda x: metric_pres(x['Barometric_Pressure']), axis=1)
                
        values['Current_Wind_Speed'] = values.apply(lambda x: metric_spd(x['Current_Wind_Speed']), axis=1)
        
        values['Current_Wind_Gust'] = values.apply(lambda x: metric_spd(x['Current_Wind_Gust']), axis=1)
        
        values['Outdoor_Temperature'] = values.apply(lambda x: metric_tmp(x['Outdoor_Temperature']), axis=1)
        
        values['Rain_Total'] = values.apply(lambda x: metric_hght(x['Rain_Total']), axis=1)
           


def readOURWEATHERData(UnitDisplay, OldUnit, Unit_toggle):
    #edit this line with the ip address of your OurWeather
    uri = 'http://192.168.0.76'

    # global Unit_Toggle, UnitDisplay, OldUnit 
    # this doesn't work very well due to some inconsistency on datertime import module issues 
    print(('readOURWEATHERData - The time is: %s' % datetime.datetime.now()))

    try:
        jsondata = getResponse(uri)       
    except:
        print("-----Can't read from OurWeather")
        df = pd.read_pickle('Stored_ourweather_dataframe.pkl')
        #convert pickled data to usable form
        #df1 = df['variables']
        #Data = df1.iloc[0:5].append(df1.iloc[10:15].append(df1.iloc[17:22]))
        #values = pd.DataFrame(Data) 
        #MetricUnits = ['NA','m','Pa','deg','kph','degC','YYYY-MM-DD hh.mm.ss','%rel','degC','mm','deg','deg','kph','kph','kph']
        #values['Units']= MetricUnits
        #if UnitDisplay == 'English':
        #    OldUnit = 'metric'
            #convert to English units
            #values['Units']= EnglishUnits
        #    ConvertUnits(UnitDisplay, OldUnit, values)
        #    print ('Converted the pickled output to English units because user wants English')
        #    print (values)
        #    values['DisplayOrder']=[12,13,4,7,6,14,1,3,2,15,9,8,10,11,5]
        #    NewData = values.sort_values(by=['DisplayOrder'])
        #    NewData1 = NewData.drop(columns=['DisplayOrder'])
        #    NewData1['Measurement'] = NewData1.index
        #    NewData2 = NewData1.rename(columns = {'variables':'Value'})
        return df
    pd.set_option("display.max_rows", 27, "display.max_columns", 10)
    pd.set_option('display.width', 180)

    data1 = pd.read_json(jsondata)
    
    print ('Read from Ourweather:')
    print ('data1: \n',data1)
    df1 = data1['variables']
    print ('Variables only df1: \n',df1)
    print ('Variables only df1: \n',df1.index)
    
    Data = df1.loc[['AirQualitySensor', 'Altitude', 'BarometricPressure', 'CurrentWindDirection', 'CurrentWindGust', 'IndoorTemperature', 'OurWeatherTime', 'OutdoorHumidity', 'OutdoorTemperature', 'RainTotal', 'WindDirectionMax', 'WindDirectionMin', 'WindGustMax','WindGustMin','WindSpeedMax']]

    print('Data =', Data)
    values = pd.DataFrame(Data)    
    #we only get metric from the arduino
    MetricUnits = ['NA','m','Pa','deg','kph','degC','YYYY-MM-DD hh.mm.ss','%rel','degC','mm','deg','deg','kph','kph','kph']
    values['Units']= MetricUnits
    
    #EnglishUnits = ['NA','ft','inHg','deg','mph','degF','YYYY-MM-DD hh.mm.ss','%rel','degF','deg','deg','mEph','mph','mph']

    if UnitDisplay == 'English':
        OldUnit = 'metric'
        #convert to English units
        #values['Units']= EnglishUnits
        ConvertUnits(UnitDisplay, OldUnit, values)
        print ('Converted the output from arduino to English units because user wants English')
        print (values)
    
    values['DisplayOrder']=[12,13,4,7,6,14,1,3,2,15,9,8,10,11,5]
    
    print (values)
    print('/n')
    NewData = values.sort_values(by=['DisplayOrder'])
    NewData1 = NewData.drop(columns=['DisplayOrder'])
    NewData1['Measurement'] = NewData1.index
    NewData2 = NewData1.rename(columns = {'variables':'Value'})
    print (NewData2)
    print('/n')

    #if Unit_toggle == 1:
    #   print ('switch units from ' + UnitDisplay + ' to ' + OldUnit)
    #   OldUnit = UnitDisplay
    #   if OldUnit == 'metric':
    #       UnitDisplay = 'English'
    #   else:
    #       UnitDisplay = 'metric'
    #   ConvertUnits(UnitDisplay, OldUnit, NewData2)
    #   print ('units have been switched from ' + OldUnit + ' to ' + UnitDisplay)
    #   Unit_toggle=0
    
    #print (NewData2)
    #print('/n')
    return NewData2

def SwitchUnits(Unit_toggle, UnitDisplay, OldUnit, values):
    #MetricUnits = ['NA','m','Pa','deg','kph','degC','YYYY-MM-DD hh.mm.ss','%rel','degC','deg','deg','kph','kph','kph']
    #EnglishUnits = ['NA','ft','inHg','deg','mph','degF','YYYY-MM-DD hh.mm.ss','%rel','degF','deg','deg','mEph','mph','mph']
    print ('In switch units before the unit toggle. Current units are: ' + UnitDisplay, '\n')
    #global Unit_Toggle, UnitDisplay, OldUnit
    if Unit_toggle == 1:
       print ('switch units from ' + UnitDisplay + ' to ' + OldUnit, '\n')
       OldUnit = UnitDisplay
       if OldUnit == 'metric':
           UnitDisplay = 'English'
       else:
           UnitDisplay = 'metric'
       print ( 'UnitDisplay =', UnitDisplay,'OldUnit = ', OldUnit, 'Unit_toggle = ', Unit_toggle,  '\n' )
       ConvertUnits(UnitDisplay, OldUnit, values)
       print ('units have been switched from ' + OldUnit + ' to ' + UnitDisplay+ '\n')
       Unit_toggle=0
    else:
        print ('do nothing because Unit_toggle = ', Unit_toggle, '\n')   
       
    return Unit_toggle, UnitDisplay, OldUnit, values
    

def SwitchUnitsCols(Unit_toggle, UnitDisplay, OldUnit, values):
    
    print ('In switch units before the unit toggle. Current units are: ' + UnitDisplay, '\n')
    
    
    Engunit = [{'OurWeather_DateTime':'Units', 'Outdoor_Temperature':'degF', 'Outdoor_Humidity':'rel%', 'Barometric_Pressure':'inHg', 'Current_Wind_Speed':'mph', 'Current_Wind_Gust':'mph', 'Current_Wind_Direction':'deg', 'Rain_Total':'in', 'Current_Air_Quality_Sensor':'NA', 'Current_Air_Quality_Qualitative':'NA', 'id':'NA'}]
    
    Metunit = [{'OurWeather_DateTime':'Units', 'Outdoor_Temperature':'degC', 'Outdoor_Humidity':'rel%', 'Barometric_Pressure':'Pa', 'Current_Wind_Speed':'kph', 'Current_Wind_Gust':'kph', 'Current_Wind_Direction':'deg', 'Rain_Total':'mm', 'Current_Air_Quality_Sensor':'NA', 'Current_Air_Quality_Qualitative':'NA', 'id':'NA'}]
       
       
    if Unit_toggle == 1:
       print ('switch units from ' + UnitDisplay + ' to ' + OldUnit, '\n')
       OldUnit = UnitDisplay
       if OldUnit == 'metric':
           UnitDisplay = 'English'
       else:
           UnitDisplay = 'metric'
       print ( 'UnitDisplay =', UnitDisplay,'OldUnit = ', OldUnit, 'Unit_toggle = ', Unit_toggle,  '\n' )
       ConvertUnitsCols(UnitDisplay, OldUnit, values)
       print ('units have been switched from ' + OldUnit + ' to ' + UnitDisplay+ '\n')
       Unit_toggle=0
       
       if UnitDisplay == 'English':
           df = pd.DataFrame(Engunit)
           df = df.append(values)
           values = df
       elif UnitDisplay == 'metric':
           df = pd.DataFrame(Metunit)
           df = df.append(values)
           values = df

       print('\n DataFrame: \n')
       print (values)
       print('\n\n')
       
    else:
        print ('do nothing because Unit_toggle = ', Unit_toggle, '\n')   
        if UnitDisplay == 'English':
           df = pd.DataFrame(Engunit)
           df = df.append(values)
           values = df
        elif UnitDisplay == 'metric':
           df = pd.DataFrame(Metunit)
           df = df.append(values)
           values = df
   
    return Unit_toggle, UnitDisplay, OldUnit, values
    

def GetSQLData(Number_of_records):
    print (Number_of_records)
    OURWEATHERtableName = 'ourweather' 
        
    #mysql user
    #edit with your database user name
    username = "YYYYY"
    #mysql Password
    #edit with your password
    password = 'XXXXXXXXX'
    #mysql Table Name   

    #edit following line
    db_connection_str = 'mysql+pymysql://root:XXXXXXXXX@localhost:3306/datalogger'
    db_connection = create_engine(db_connection_str)
    
    #our units row
    unit = [{'OurWeather_DateTime':'Units', 'Outdoor_Temperature':'degC', 'Outdoor_Humidity':'rel%', 'Barometric_Pressure':'Pa', 'Current_Wind_Speed':'kph', 'Current_Wind_Gust':'kph', 'Current_Wind_Direction':'deg', 'Rain_Total':'mm', 'Current_Air_Quality_Sensor':'NA', 'Current_Air_Quality_Qualitative':'NA', 'id':'NA', 'HeatIndex':'degC', 'WindChill':'degC'}]
    dfunits = pd.DataFrame(unit)

    if (Number_of_records==0):
        dfalt = pd.read_sql('(SELECT OurWeather_DateTime, Outdoor_Temperature, Outdoor_Humidity, Barometric_Pressure, Current_Wind_Speed, Current_Wind_Gust, Current_Wind_Direction, Rain_Total, Current_Air_Quality_Sensor, Current_Air_Quality_Qualitative, id FROM ourweather ORDER BY id DESC) ORDER BY id ASC', con=db_connection)
        print ('Got here to ALL query')
    
    else:
        dfalt = pd.read_sql('(SELECT OurWeather_DateTime, Outdoor_Temperature, Outdoor_Humidity, Barometric_Pressure, Current_Wind_Speed, Current_Wind_Gust, Current_Wind_Direction, Rain_Total, Current_Air_Quality_Sensor, Current_Air_Quality_Qualitative, id FROM '+OURWEATHERtableName+' ORDER BY id DESC LIMIT '+ str(Number_of_records) + ') ORDER BY id ASC', con=db_connection)
        print('Never got to all query')
    
    #add heat index and windchill
    dfalt = AddHeatIndexWindChill(dfalt)
    # append the data to the unit row
    
    df = dfunits.append(dfalt)
    
    print('\n DataFrame: \n')
    print (df)
    print('\n\n')
    
    print('\n DataFrame: \n')
    print (dfalt)
    print('\n\n')
    
    return df, dfalt

def HeatIndex(dfalt):
    # T in deg F
    # H is realtive humidity in percent
    # Assume T is coming in DegC and put it in degF
    try: 
        TC = dfalt.Outdoor_Temperature
        RH = dfalt.Outdoor_Humidity
    except AttributeError:
        TC = dfalt.loc['OutdoorTemperature','Value']
        RH = dfalt.loc['OutdoorHumidity','Value']
            
    #print (TC, RH)
        
    T = (9/5*TC + 32)

    HI = 0.5 * (T + 61.0 + ((T-68.0)*1.2) + (RH*0.094))
    
    #print ('Temp: ',T, 'HI: ',HI)
    #print ((HI+T)/2)

    if (HI+T)/2 >= 80: 
        HI= -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
        
        if (RH < 13) and (80 <= T <= 122):
            ADJ = ((13-RH)/4)*SQRT((17-ABS(T-95.))/17)
            HI = HI - ADJ
        
        elif (RH > 85) and (80 <= T <= 87):
            ADJ = ((RH-85)/10) * ((87-T)/5)
            HI = HI + ADJ
    
    # convert back to degC
    HIC = (HI - 32)*5/9       

    if (HIC < TC):
        HIC = TC

    return HIC

def WindChill(dfalt):
    # T is temperature in deg F
    # V is wind speed in mph
    # Assume T is coming in DegC; put it in degF
    # assume V is coming in in kph, put it in mph
    try: 
        TC = dfalt.Outdoor_Temperature
        VK = dfalt.Current_Wind_Speed
    except AttributeError:
        TC = dfalt.loc['OutdoorTemperature','Value']
        VK = dfalt.loc['CurrentWindGust','Value']
    
    #print (TC, VK)
    T = (9/5*TC + 32)
    V = VK * 0.62137

    if (T < 50) and (V >= 3):
        WC = 35.74 + 0.6125*T - 35.75 * V ** 0.16 + 0.4275 * T * V ** 0.16

    else:
        WC = T
    
    # convert back to degC
    WCC = (WC - 32)*5/9 
    
    if (WCC > TC):
        WCC = TC

    return WCC

def AddHeatIndexWindChill(dfalt):
    
    #dfSQLall['HeatIndex'] = HeatIndex(dfSQLall['Outdoor_Temperature'],dfSQLall['Outdoor_Humidity'])

    #dfSQLall['WindChill'] = WindCHill(dfSQLall['Outdoor_Temperature'],dfSQLall['Current_Wind_Speed'])

    dfalt['HeatIndex'] = dfalt.apply(HeatIndex, axis =1)

    dfalt['WindChill'] = dfalt.apply(WindChill, axis =1)

    return dfalt

def AddHeatIndexWindChilldf(dfalt):
    
    #dfSQLall['HeatIndex'] = HeatIndex(dfSQLall['Outdoor_Temperature'],dfSQLall['Outdoor_Humidity'])

    #dfSQLall['WindChill'] = WindCHill(dfSQLall['Outdoor_Temperature'],dfSQLall['Current_Wind_Speed'])

    dfalt['HeatIndex'] = dfalt.apply(HeatIndex, axis =0)

    dfalt['WindChill'] = dfalt.apply(WindChill, axis =0)

    return dfalt