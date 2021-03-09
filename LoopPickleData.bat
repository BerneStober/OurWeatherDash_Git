rem this file is run using windows scheduler to do the almost real time data grab
rem running this way avoids holding up the Dash app waiting for ourweather to respond

cd C:\Users\YYYYY\source\repos\OurWeatherDashV3
SET /A XCOUNT=1
:here
	Echo run python from command line   %XCOUNT%
	
SET /A XCOUNT+=1

C:\Users\YYYYY\AppData\Local\Programs\Python\Python38\python C:\Users\YYYYY\source\repos\OurWeatherDashV3\Pickle_data_loop2.py

 
TIMEOUT 60

rem GOTO:here