import dash
import os
# change this below to where this code is located
os.chdir(r'C:\Users\berny\source\repos\OurWeatherDash')
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol
import pandas as pd
import Dash_functions2
import plotly.express as px
from dash.dependencies import Input, Output, State
import datetime
import Records

pd.set_option("display.max_rows", 20, "display.max_columns", 8)
pd.set_option('display.width', 100)

f = open("DashTabsNew10_debug_prints.txt", "a", encoding='utf-8')
#units always start as metric

# i use a pickle with a seprate routine that reads and stores the weather data in a
# pickle because sometimes the data fetch from our weather is very slow
# the pickle_data_loop.py script does the pickle storage; it is run with windows scheduler
# so it is independent of both the SQL data storage and this Dash program for data display 
Use_pickle = 1
Unit_toggle=0
UnitDisplay = 'metric'
OldUnit = 'English'
# use 0 below to get all records
dfdisplay_all, dfSQLall = Dash_functions2.GetSQLData(0)

dfdisplay, dfSQL = Dash_functions2.GetSQLData(3000)

DFRecords = Records.Records_trends(dfSQLall)

print (DFRecords, '\n', file=f)

# either read the pickle or get the data from the Ourweather device directly
if Use_pickle == 1:
    df = pd.read_pickle('Stored_ourweather_dataframe.pkl')
else:
    df = Dash_functions2.readOURWEATHERData(UnitDisplay, OldUnit, Unit_toggle)
    df.to_pickle('Stored_ourweather_dataframe.pkl')

df = df[['Measurement','Value','Units']]
print (df, file=f)
print (df.to_dict('records'), file=f)

#get dates by dividing the dfSQL into eight equal date sectors
#MinDate = dfSQLall.head(1)['OurWeather_DateTime'].dt.date
#MaxDate = dfSQLall.tail(1)['OurWeather_DateTime'].dt.date
MinDate = pd.Timestamp.date(dfSQLall.iloc[1,0])
MaxDate = max(dfSQLall['OurWeather_DateTime'].dt.date)
#print (MinDate, MaxDate)

DateSection = (MaxDate - MinDate)/8
#print (DateSection)

# not sure if this needed, dummy dates to define it
dates = ['2015-02-17', '2015-05-17', '2015-08-17', '2015-11-17',
         '2016-02-17', '2016-05-17', '2016-08-17', '2016-11-17', '2017-02-17']

i = 0
while i < 9:
    dates[i] = MinDate + i * DateSection
    i += 1 

figRain_Total = px.line(dfSQLall, x='OurWeather_DateTime', y='Rain_Total', title='Rain Time Series')

figOutdoor_Temperature = px.line(dfSQLall, x='OurWeather_DateTime', y='Outdoor_Temperature', title='Outdoor Temperature Time Series')

figOutdoor_Humidity = px.line(dfSQLall, x='OurWeather_DateTime', y='Outdoor_Humidity', title='Humidity Time Series')

figBarometric_Pressure = px.line(dfSQLall, x='OurWeather_DateTime', y='Barometric_Pressure', title='Barometric Pressure Time Series')

app = dash.Dash(name = __name__)
app.config['suppress_callback_exceptions'] = True


app.layout = html.Div([
    # you will want to change this text to your weather station
    html.H1('Welcome to the XXXXXX Weather Station at XXXXXXX. Located in XXXXXXXX.', style={'text-align':'center','color': 'white','background-color': 'black'}),
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Current weather',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Weather Table',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Weather graphs',
                value='tab-3', className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Records and Trends',
                value='tab-4',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes')
])


@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Button('Update', id='btn1', n_clicks=0),
            html.Button('ConvertUnits', id='btn2', n_clicks=0),
            html.Div(id='container-button-basic',
             children='Default units are Metric. Values in pink are most likely bad data.'),
            
            dash_table.DataTable(
            id='table',
            data=df.to_dict('records'),
            
            columns=[{
            'id': 'Measurement',
            'name': 'Measurement',
            'type': 'text'
            }, {
            'id': 'Value',
            'name': 'Value',
            'type': 'numeric',
            'format': Format(
                precision=2,
                scheme=Scheme.fixed
                 ),
            }, {
            'id': 'Units',
            'name': 'Unit',
            'type': 'text'
            },],
            
            style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'fontWeight': 'bold'
            },
            style_cell={'textAlign': 'center','backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'},
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Measurement'},
                    'textAlign': 'left',
                    'if': {'column_id': 'Value'},
                    'textAlign': 'center',
                    'if': {'column_id': 'Units'},
                    'textAlign': 'center',
                }],
            style_data_conditional=[
            {'if': {
                'row_index': 14,  # number | 'odd' | 'even'
                'column_id': 'Value'
            },
            'backgroundColor': 'hotpink',
            'color': 'white'
            },
            {'if': {
                'row_index': 11,  # number | 'odd' | 'even'
                'column_id': 'Value'
            },
            'backgroundColor': 'hotpink',
            'color': 'white'
            }
            ]
            )

        ])
    elif tab == 'tab-2':
        dfdisplay, dfSQL = Dash_functions2.GetSQLData(3000)
        return html.Div([
            html.Button('UnitConversion', id='btn4', n_clicks=0),
            dash_table.DataTable(
                id='tableSQL',
                columns=[{'id': 'OurWeather_DateTime',
                'name': 'OurWeather_DateTime','type': 'text',},
                {'id': 'Outdoor_Temperature','name': 'Temperature','type': 'numeric',
                'format': Format(precision=2,scheme=Scheme.fixed),}, 
                {'id': 'Outdoor_Humidity','name': 'Humidity','type': 'numeric',
                'format': Format(precision=2,scheme=Scheme.fixed),}, 
                {'id': 'Barometric_Pressure','name': 'Barometric Pressure','type': 'numeric',
                'format': Format(precision=2,scheme=Scheme.fixed),},          
                {'id': 'Current_Wind_Speed','name': 'Wind Speed','type': 'numeric',
                'format': Format(precision=2,scheme=Scheme.fixed),}, 
                {'id': 'Current_Wind_Gust','name': 'Wind Gust','type': 'numeric',
                'format': Format(precision=2,scheme=Scheme.fixed),}, 
                {'id': 'Current_Wind_Direction','name': 'Wind Direction','type': 'numeric',
                'format': Format(precision=2,scheme=Scheme.fixed),}, 
                {'id': 'Rain_Total','name': 'Rain Total','type': 'numeric',
                'format': Format(precision=2,scheme=Scheme.fixed),},
                {'id': 'Current_Air_Quality_Sensor','name': 'Air Quality Sensor','type': 'numeric', 
                'format': Format(precision=2,scheme=Scheme.fixed),}, 
                {'id': 'Current_Air_Quality_Qualitative','name': 'Air Quality','type': 'numeric',
                }, 
                ],
                data=dfdisplay.to_dict('records'),
                fixed_rows={'headers': True, 'data': 1},
                style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                style_cell={'textAlign': 'center','backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'},
                style_cell_conditional=[
                {'if': {'column_id': 'OurWeather_DateTime'},'textAlign': 'center','width':'11%'},
                {'if': {'column_id': 'Outdoor_Temperature'},'textAlign': 'center','width':'7%'},
                {'if': {'column_id': 'Outdoor_Humidity'},'textAlign': 'center','width':'6%'},
                {'if': {'column_id': 'Barometric_Pressure'},'textAlign': 'center','width':'11%'},
                {'if': {'column_id': 'Current_Wind_Speed'},'textAlign': 'center','width':'6%'},
                {'if': {'column_id': 'Current_Wind_Gust'},'textAlign': 'center','width':'6%'},
                {'if': {'column_id': 'Current_Wind_Direction'},'textAlign': 'center','width':'8%'},
                {'if': {'column_id': 'Rain_Total'},'textAlign': 'center','width':'6%'},
                {'if': {'column_id': 'Current_Air_Quality_Sensor'},'textAlign': 'center','width':'11%'},
                {'if': {'column_id': 'Current_Air_Quality_Qualitative'},'textAlign': 'center','width':'7%'},
                {'if': {'column_id': 'id'},'textAlign': 'center','width':'3%' },
                ]
            )
        ])
    elif tab == 'tab-3':
        return html.Div(children=[
            html.P([
                html.Label("Time Period"),
                dcc.RangeSlider(id = 'slider',
                                marks = {i : dates[i] for i in range(0, 9)},
                                    min = 0,
                                    max = 8,
                                    value = [0, 8])
                    ], style = {'width' : '80%',
                                'fontSize' : '20px',
                                'padding-left' : '100px'}),
                                
                    
            html.Div([
                dcc.Graph(id='Outdoor_Temperature',figure=figOutdoor_Temperature),
                ]),
                
                        
         # New Div for all elements in the new 'row' of the page    
            
            html.Div([
                 dcc.Graph(id='Outdoor_Humidity',figure=figOutdoor_Humidity),
                 ]),
        # New Div for all elements in the new 'row' of the page   
            
            html.Div([
                dcc.Graph(id='Barometric_Pressure',figure=figBarometric_Pressure),
                ]),
        # New Div for all elements in the new 'row' of the page  
            
            html.Div([dcc.Graph(id='Rain_Total',figure=figRain_Total),  
                ]),
              
            ])
    elif tab == 'tab-4':
        return html.Div([
            html.Button('UnitConversion', id='btn3', n_clicks=0),
            dash_table.DataTable(
                id ='records',
                
                data = DFRecords.to_dict('records'),
                
                columns=[{
            'id': 'Item',
            'name': 'Item',
            'type': 'text',
            }, {
            'id': 'Value',
            'name': 'Value',
            'type': 'numeric',
            'format': Format(
                precision=2,
                scheme=Scheme.fixed
                 ),
            
            }, {
            'id': 'Units',
            'name': 'Units',
            'type': 'text'
            },
                         {
            'id': 'Date Occured',
            'name': 'Date Occured',
            'type': 'text'
            },],
                fixed_rows={'headers': True, 'data': 1},
                style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                style_cell={'textAlign': 'center','backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'},
                style_cell_conditional=[
                {'if': {'column_id': 'Value'},'textAlign': 'center','width':'30%'},
                {'if': {'column_id': 'Units'},'textAlign': 'center','width':'15%' },
                {'if': {'column_id': 'Item'},'textAlign': 'left', 'width':'30%'},
                {'if': {'column_id': 'Date Occured'},'textAlign': 'center', 'width':'25%'}
                ]
            )
        ])

#Add callback functions
@app.callback(Output('Outdoor_Temperature', 'figure'),
             [Input('slider', 'value')])
def update_figure(X):
    
    dfSQLall2 = dfSQLall[(dfSQLall.OurWeather_DateTime.dt.date > dates[X[0]]) & (dfSQLall.OurWeather_DateTime.dt.date < dates[X[1]])]
    
    fig = figOutdoor_Temperature = px.line(dfSQLall2, x='OurWeather_DateTime', y='Outdoor_Temperature', title='Outdoor Temperature Time Series')
    
    return fig

@app.callback(Output('Outdoor_Humidity', 'figure'),
             [Input('slider', 'value')])
def update_figure(X):
    
    dfSQLall2 = dfSQLall[(dfSQLall.OurWeather_DateTime.dt.date > dates[X[0]]) & (dfSQLall.OurWeather_DateTime.dt.date < dates[X[1]])]
    
    fig = figOutdoor_Humidity = px.line(dfSQLall2, x='OurWeather_DateTime', y='Outdoor_Humidity', title='Outdoor Humidity Time Series')
    
    return fig

@app.callback(Output('Barometric_Pressure', 'figure'),
             [Input('slider', 'value')])
def update_figure(X):
       
    dfSQLall2 = dfSQLall[(dfSQLall.OurWeather_DateTime.dt.date > dates[X[0]]) & (dfSQLall.OurWeather_DateTime.dt.date < dates[X[1]])]
    
    print (dfSQLall['Barometric_Pressure'], dfSQLall2['Barometric_Pressure'], file=f)
    
    fig = figBarometric_Pressure = px.line(dfSQLall2, x='OurWeather_DateTime', y='Barometric_Pressure', title='Barometric_Pressure Time Series')
    
    return fig

@app.callback(Output('Rain_Total', 'figure'),
             [Input('slider', 'value')])
def update_figure(X):
    
    dfSQLall2 = dfSQLall[(dfSQLall.OurWeather_DateTime.dt.date > dates[X[0]]) & (dfSQLall.OurWeather_DateTime.dt.date < dates[X[1]])]
    
    fig = figRain_Total = px.line(dfSQLall2, x='OurWeather_DateTime', y='Rain_Total', title='Rain_Total Time Series')
    
    return fig

@app.callback(
    Output('table', 'data'),
    Input('btn1', 'n_clicks'),
    Input('btn2', 'n_clicks')
    )
def updateTable(btn,btn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print (changed_id, file=f)
    global Unit_Toggle, UnitDisplay, OldUnit, Use_pickle, df
    if 'btn1' in changed_id:
        Unit_toggle = 0
        
        if Use_pickle == 1:
            df = pd.read_pickle('Stored_ourweather_dataframe.pkl')
        else:
            df = Dash_functions2.readOURWEATHERData(UnitDisplay, OldUnit, Unit_toggle)

        
        df = df[['Measurement','Value','Units']]
        print ('In update data button', '\n', df, file=f)
        
        return df.to_dict('records')
    elif 'btn2' in changed_id:
        #toggle units
        Unit_toggle=1
        Unit_toggle, UnitDisplay, OldUnit, df = Dash_functions2.SwitchUnits(Unit_toggle, UnitDisplay, OldUnit, df)
        print (df, '\n', 'UnitDisplay =', UnitDisplay,'OldUnit = ', OldUnit, 'Unit_toggle = ', Unit_toggle, file=f)
        
        print ('In toggle units data button', '\n', df, file=f)
        
        return df.to_dict('records')
    else:
        #code added to try to force initial display
        Unit_toggle = 0
        if Use_pickle == 1:
            df = pd.read_pickle('Stored_ourweather_dataframe.pkl')
        else:
            df = Dash_functions2.readOURWEATHERData(UnitDisplay, OldUnit, Unit_toggle)
        df = df[['Measurement','Value','Units']]
        print ('In update data button', '\n', df, file=f)
        
        return df.to_dict('records')

@app.callback(
    Output('records', 'data'),
    Input('btn3', 'n_clicks')
    )
def updateRecords(btn3):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print (changed_id, file=f)
    global Unit_Toggle, UnitDisplay, OldUnit, DFRecords
    if 'btn3' in changed_id:
        #toggle units
        Unit_toggle=1
        Unit_toggle, UnitDisplay, OldUnit, DFRecords = Dash_functions2.SwitchUnits(Unit_toggle, UnitDisplay, OldUnit, DFRecords)
        print (DFRecords, '\n', 'UnitDisplay =', UnitDisplay,'OldUnit = ', OldUnit, 'Unit_toggle = ', Unit_toggle, file=f)
        
        print ('In toggle units data button', '\n', df, file=f)
        
        return DFRecords.to_dict('records')
        
    else:
        
        return DFRecords.to_dict('records')

@app.callback(
    Output('tableSQL', 'data'),
    Input('btn4', 'n_clicks')
    )
def updateRecords(btn4):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print (changed_id, file=f)
    global Unit_Toggle, UnitDisplay, OldUnit, dfdisplay
    if 'btn4' in changed_id:
        #toggle units
        Unit_toggle=1
        Unit_toggle, UnitDisplay, OldUnit, dfdisplay = Dash_functions2.SwitchUnitsCols(Unit_toggle, UnitDisplay, OldUnit, dfSQL)
        print (dfdisplay, '\n', 'UnitDisplay =', UnitDisplay,'OldUnit = ', OldUnit, 'Unit_toggle = ', Unit_toggle, file=f)
        
        print ('In toggle units data button', '\n', df, file=f)
        
        return dfdisplay.to_dict('records')
        
    else:
        
        return dfdisplay.to_dict('records')

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

f.close()
