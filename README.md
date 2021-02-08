# OurWeatherDash_Git
Code for a Dash based weather reporting software for the Ourweather weather station kit from switchdoc.com .  You can check out the results of this program at 
http://markensglenweather.dyndnss.net/ . All of this was developed totally with freeware. To run this program you have to have installed MySql and use my 
other Git repository to develop a database of your weather data. You will also need to install Python. It was developed in Python 3.8 but also runs in 
Python 3.7 using Visual studio in a windows 10 based system. You will of course need to pip install all the modules required in the import statements. 

The program can be run on a local host but to run it on a website from your local server I recommend you install WAMP and use DYNDNSS.NET for free 
domain names. Installing WAMP is covered by many websites which can be found with Google or Bing. WAMP installation can be difficult and requires
some knowledge of the Windows system, including VC++ distrbutables installation, turning off IIS, setting the firewall properly, and setting the apache conf and vhosts conf correctly. I would approach getting WAMP running on your Windows machine as a separate project.

It may not work if you use other means to publish Dash programs because it needs access to your local network to read the 
OurWeather data. 

Please read through all the comments because you will need to follow the instructions there to customize your code with user names, passwords, URI's and 
paths.

If you add enhancements please do share them!
