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

# set display options for dataframes
pd.set_option("display.max_rows", 20, "display.max_columns", 8)
pd.set_option('display.width', 100)

#debug file
f = open("DashTabsNew10_debug_prints.txt", "a", encoding='utf-8')

def getResponse(uri):
    operUrl = urllib.request.urlopen(uri)
    if(operUrl.getcode()==200):
        data = operUrl.read()
        #jsonData = json.loads(data)
    else:
        print("Error receiving data", operUrl.getcode(), file=f)
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
    metric_tmp = lambda x: (x - 32)/(9/5)
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
    metric_tmp = lambda x: (x - 32)/(9/5)
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
           


#adjust the uri to the location on your local network where your Ourweather is located
def readOURWEATHERData(UnitDisplay, OldUnit, Unit_toggle):
    uri = 'http://192.168.0.117'

    print(('readOURWEATHERData - The time is: %s' % datetime.datetime.now()), file=f)

    try:
        jsondata = getResponse(uri)       
    except:
        print("-----Can't read from OurWeather", file=f)
        df = pd.read_pickle('Stored_ourweather_dataframe.pkl')
        return df

    data1 = pd.read_json(jsondata)
    print ('Read from Ourweather:', file=f)
    print (data1, file=f)
    df1 = data1['variables']
    Data = df1.iloc[0:5].append(df1.iloc[10:15].append(df1.iloc[17:22]))
    print(Data, file=f)
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
        print ('Converted the output from arduino to English units because user wants English', file=f)
        print (values, file=f)
    
    values['DisplayOrder']=[12,13,4,7,6,14,1,3,2,15,9,8,10,11,5]
    
    print (values, file=f)
    print('/n', file=f)
    NewData = values.sort_values(by=['DisplayOrder'])
    NewData1 = NewData.drop(columns=['DisplayOrder'])
    NewData1['Measurement'] = NewData1.index
    NewData2 = NewData1.rename(columns = {'variables':'Value'})
    print (NewData2, file=f)
    print('/n', file=f)

    return NewData2

def SwitchUnits(Unit_toggle, UnitDisplay, OldUnit, values):
    #MetricUnits = ['NA','m','Pa','deg','kph','degC','YYYY-MM-DD hh.mm.ss','%rel','degC','deg','deg','kph','kph','kph']
    #EnglishUnits = ['NA','ft','inHg','deg','mph','degF','YYYY-MM-DD hh.mm.ss','%rel','degF','deg','deg','mEph','mph','mph']
    
    print ('In switch units before the unit toggle. Current units are: ' + UnitDisplay, '\n', file=f)
    
    if Unit_toggle == 1:
       print ('switch units from ' + UnitDisplay + ' to ' + OldUnit, '\n', file=f)
       OldUnit = UnitDisplay
       if OldUnit == 'metric':
           UnitDisplay = 'English'
       else:
           UnitDisplay = 'metric'
       print ( 'UnitDisplay =', UnitDisplay,'OldUnit = ', OldUnit, 'Unit_toggle = ', Unit_toggle,  '\n', file=f )
       ConvertUnits(UnitDisplay, OldUnit, values)
       print ('units have been switched from ' + OldUnit + ' to ' + UnitDisplay+ '\n', file=f)
       Unit_toggle=0
    else:
        print ('do nothing because Unit_toggle = ', Unit_toggle, '\n', file=f)   
       
    return Unit_toggle, UnitDisplay, OldUnit, values
    

def SwitchUnitsCols(Unit_toggle, UnitDisplay, OldUnit, values):
    #MetricUnits = ['NA','m','Pa','deg','kph','degC','YYYY-MM-DD hh.mm.ss','%rel','degC','deg','deg','kph','kph','kph']
    #EnglishUnits = ['NA','ft','inHg','deg','mph','degF','YYYY-MM-DD hh.mm.ss','%rel','degF','deg','deg','mEph','mph','mph']
    print ('In switch units before the unit toggle. Current units are: ' + UnitDisplay, '\n', file=f)
    #global Unit_Toggle, UnitDisplay, OldUnit
    
    Engunit = [{'OurWeather_DateTime':'Units', 'Outdoor_Temperature':'degF', 'Outdoor_Humidity':'rel%', 'Barometric_Pressure':'inHg', 'Current_Wind_Speed':'mph', 'Current_Wind_Gust':'mph', 'Current_Wind_Direction':'deg', 'Rain_Total':'in', 'Current_Air_Quality_Sensor':'NA', 'Current_Air_Quality_Qualitative':'NA', 'id':'NA'}]
    
    Metunit = [{'OurWeather_DateTime':'Units', 'Outdoor_Temperature':'degC', 'Outdoor_Humidity':'rel%', 'Barometric_Pressure':'Pa', 'Current_Wind_Speed':'kph', 'Current_Wind_Gust':'kph', 'Current_Wind_Direction':'deg', 'Rain_Total':'mm', 'Current_Air_Quality_Sensor':'NA', 'Current_Air_Quality_Qualitative':'NA', 'id':'NA'}]
       
       
    if Unit_toggle == 1:
       print ('switch units from ' + UnitDisplay + ' to ' + OldUnit, '\n', file=f)
       OldUnit = UnitDisplay
       if OldUnit == 'metric':
           UnitDisplay = 'English'
       else:
           UnitDisplay = 'metric'
       print ( 'UnitDisplay =', UnitDisplay,'OldUnit = ', OldUnit, 'Unit_toggle = ', Unit_toggle,  '\n', file=f )
       ConvertUnitsCols(UnitDisplay, OldUnit, values)
       print ('units have been switched from ' + OldUnit + ' to ' + UnitDisplay+ '\n', file=f)
       Unit_toggle=0
       
       if UnitDisplay == 'English':
           df = pd.DataFrame(Engunit)
           df = df.append(values)
           values = df
       elif UnitDisplay == 'metric':
           df = pd.DataFrame(Metunit)
           df = df.append(values)
           values = df

       print('\n DataFrame: \n', file=f)
       print (values, file=f)
       print('\n\n', file=f)
       
    else:
        print ('do nothing because Unit_toggle = ', Unit_toggle, '\n', file=f)   
        if UnitDisplay == 'English':
           df = pd.DataFrame(Engunit)
           df = df.append(values)
           values = df
        elif UnitDisplay == 'metric':
           df = pd.DataFrame(Metunit)
           df = df.append(values)
           values = df
   
    return Unit_toggle, UnitDisplay, OldUnit, values
    
# put in the information for your MySQL database below
def GetSQLData(Number_of_records):
    print (Number_of_records, file=f)
    # your table where you are storing the data
    OURWEATHERtableName = 'ourweather' 
        
    #mysql user
    username = "XXXXX"
    #mysql Password
    password = 'XXXXXXXX'
    #mysql Table Name   

    # put in your password below in place of X's
    db_connection_str = 'mysql+pymysql://root:XXXXXXXX@localhost:3306/datalogger'
    db_connection = create_engine(db_connection_str)
    
    #our units row
    unit = [{'OurWeather_DateTime':'Units', 'Outdoor_Temperature':'degC', 'Outdoor_Humidity':'rel%', 'Barometric_Pressure':'Pa', 'Current_Wind_Speed':'kph', 'Current_Wind_Gust':'kph', 'Current_Wind_Direction':'deg', 'Rain_Total':'mm', 'Current_Air_Quality_Sensor':'NA', 'Current_Air_Quality_Qualitative':'NA', 'id':'NA'}]
    df = pd.DataFrame(unit)

    if (Number_of_records==0):
        dfalt = pd.read_sql('(SELECT OurWeather_DateTime, Outdoor_Temperature, Outdoor_Humidity, Barometric_Pressure, Current_Wind_Speed, Current_Wind_Gust, Current_Wind_Direction, Rain_Total, Current_Air_Quality_Sensor, Current_Air_Quality_Qualitative, id FROM ourweather ORDER BY id DESC) ORDER BY id ASC', con=db_connection)
        print ('Got here to ALL query')
    
    else:
        dfalt = pd.read_sql('(SELECT OurWeather_DateTime, Outdoor_Temperature, Outdoor_Humidity, Barometric_Pressure, Current_Wind_Speed, Current_Wind_Gust, Current_Wind_Direction, Rain_Total, Current_Air_Quality_Sensor, Current_Air_Quality_Qualitative, id FROM '+OURWEATHERtableName+' ORDER BY id DESC LIMIT '+ str(Number_of_records) + ') ORDER BY id ASC', con=db_connection)
        print('Never got to all query')
    
    #correct barometric pressure when unit changed
    # do it before adding units! otherwise the unit being a str creates an error!
    # you can delete this code if you don't have dataerrors that need to be corrected
    correct_BP = lambda x: 0.944649*x
    Break_in_BP = datetime.datetime(2020,6,1)

    def BP_Correct(x1):
        return 0.944649*x1

    #using lambda function to change based on date
    dfalt['Barometric_Pressure'] = dfalt.apply(lambda x: BP_Correct(x['Barometric_Pressure']) if x['OurWeather_DateTime'] < Break_in_BP else x['Barometric_Pressure'], axis=1)
    

    # append the data to the unit row
    df = df.append(dfalt)
    
    print('\n DataFrame: \n', file=f)
    print (df, file=f)
    print('\n\n', file=f)

    
    print (df['Barometric_Pressure'], file=f)
    #Dataframe = readOURWEATHERData(username, password)

    return df, dfalt
