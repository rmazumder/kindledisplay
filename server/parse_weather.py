import myql
import urllib3
from xml.dom import minidom
import datetime
import codecs
import sys
import requests
import time

def getCardinal(angle):
	directions = 8
	degree = 360 / directions
	angle = angle + degree/2
	if angle >= (0 * degree) and angle < (1 * degree):
		return "N"
	if angle >= (1 * degree) and angle < (2 * degree):
		return "NE"
	if angle >= (2 * degree) and angle < (3 * degree):
		return "E"
	if angle >= (3 * degree) and angle < (4 * degree):
		return "SE"
	if angle >= (4 * degree) and angle < (5 * degree):
		return "S"
	if angle >= (5 * degree) and angle < (6 * degree):
		return "SW"
	if angle >= (6 * degree) and angle < (7 * degree):
		return "W"
	if angle >= (7 * degree) and angle < (8 * degree):
		return "NW"
	return "N"

#Code of my city
CODE = "2400849"
#Change to false if you want Fahrenheit and mph
METRIC = True

from myql.utils import pretty_json, pretty_xml
yql = myql.MYQL(format='xml', community=True)

#can't trust windchill if specified in celsius (must parse from fahrenheit)
weather_xml = yql.raw_query('select * from weather.forecast where woeid = ' + CODE + ' and u ="f"')
dom = minidom.parseString(weather_xml.content)
xml_wind = dom.getElementsByTagName('yweather:wind')
wind = xml_wind[0]
chill = wind.getAttribute('chill')


if METRIC:
     weather_xml = yql.raw_query('select * from weather.forecast where woeid = ' + CODE + ' and u ="f"')
     chill = str(int(round((float(chill) - 32) / 1.8)))
     dom = minidom.parseString(weather_xml.content)

#Get weather Tags
xml_current = dom.getElementsByTagName('yweather:condition')
xml_temperatures = dom.getElementsByTagName('yweather:forecast')
xml_wind = dom.getElementsByTagName('yweather:wind')
xml_location = dom.getElementsByTagName('yweather:location')
xml_atmos = dom.getElementsByTagName('yweather:atmosphere')
xml_units = dom.getElementsByTagName('yweather:units')
xml_astron = dom.getElementsByTagName('yweather:astronomy')
#Get today Tag
current = xml_current[0]
today = xml_temperatures[0]
future1 = xml_temperatures[1]
future2 = xml_temperatures[2]
future3 = xml_temperatures[3]
future4 = xml_temperatures[4]

wind = xml_wind[0]
location = xml_location[0]
atmos = xml_atmos[0]
units = xml_units[0]
astron = xml_astron[0]
#Get info
status = current.getAttribute('text')
image = current.getAttribute('code')
date = current.getAttribute('date')
concisedates = date.split()
concisedate = ' '.join([concisedates[2],concisedates[1].lstrip("0")])
concisetime = ' '.join([concisedates[4],concisedates[5]])
concisetime = concisetime + ' ('+concisedates[0].rstrip(",")+')';
temp = current.getAttribute('temp')
low = today.getAttribute('low')
high = today.getAttribute('high')

future1low = future1.getAttribute('low')
future1high = future1.getAttribute('high')
future1day = future1.getAttribute('day')

future2low = future2.getAttribute('low')
future2high = future2.getAttribute('high')
future2day = future2.getAttribute('day')

future3low = future3.getAttribute('low')
future3high = future3.getAttribute('high')
future3day = future3.getAttribute('day')

future4low = future4.getAttribute('low')
future4high = future4.getAttribute('high')
future4day = future4.getAttribute('day')



#chill = wind.getAttribute('chill')
direction = wind.getAttribute('direction')
speed = wind.getAttribute('speed')
humidity = atmos.getAttribute('humidity')
pressure = atmos.getAttribute('pressure')
pressureunit = units.getAttribute('pressure')
city = location.getAttribute('city')
sunset = astron.getAttribute('sunset')
sunrise = astron.getAttribute('sunrise')
image_url = 'assets/' + image + '.png'
f1image_url = 'assets/' + future1.getAttribute('code') + '.png'
f2image_url = 'assets/' + future2.getAttribute('code') + '.png'
f3image_url = 'assets/' + future3.getAttribute('code') + '.png'
f4image_url = 'assets/' + future4.getAttribute('code') + '.png'
# Open SVG to process
output = codecs.open('template.svg', 'r', encoding='utf-8').read()


# Insert icons and temperatures
output = output.replace('TODAY',concisedate)
output = output.replace('TIME',concisetime)
output = output.replace('CITY',city)
output = output.replace('HUMID',humidity)
output = output.replace('ICON_ONE',image_url)
output = output.replace('HIGH_ONE',high)

output = output.replace('F1',future1day+":"+future1low+"/"+future1high)
output = output.replace('F2',future2day+":"+future2low+"/"+future2high)
output = output.replace('F3',future3day+":"+future3low+"/"+future3high)
output = output.replace('F4',future4day+":"+future4low+"/"+future4high)
output = output.replace('ICON_FU1',f1image_url)
output = output.replace('ICON_FU2',f2image_url)
output = output.replace('ICON_FU3',f3image_url)
output = output.replace('ICON_FU4',f4image_url)


output = output.replace('CURR_TEMP',temp)
output = output.replace('LOW_ONE',low)
output = output.replace('SUNSET',sunset.rstrip(' pm'))
output = output.replace('SUNRISE',sunrise.rstrip(' am'))
#status = status + '('+concisedates[0]+')';
output = output.replace('STATUS',status)
if chill>=temp:
     output = output.replace('black','white')
     output = output.replace('TEMPYCOORD','310')
else:
     output = output.replace('TEMPYCOORD','270')


output = output.replace('SPEED',str(int(round(float(speed)))))
output = output.replace('NESW',getCardinal(float(direction)))
if METRIC:
    output = output.replace('UNIT','km/h')
else:
    output = output.replace('UNIT','mph')
    
    
    
# exchange rate
if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlopen

from bs4 import BeautifulSoup
quote_page = 'https://www.remitly.com/us/en/india'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
remitly_box = soup.findAll('span', attrs={'class': 'remitly-rate'})[1]
xoom_box = soup.findAll('span', attrs={'class': 'competitor-rate'})[0]

remitly = remitly_box.text.strip()
xoom = xoom_box.text.strip()
output = output.replace('REMITLY',remitly)
output = output.replace('XOOM',xoom)

quote_page = 'http://entryindia.com/exchange_rates'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
tbody = soup.findAll('tbody', attrs={'id': 'ei_bxr_table'})[0]
trs = tbody.findAll('tr')
wurate = 0
riarate = 0
for tr in trs:
    
    provider = tr.findAll('td')[0].find('p').text.strip()
    rate = tr.findAll('td')[1].text.strip().rstrip('Fixed').rstrip('Indicativ')
    if(provider == 'Western Union'):
        wurate = rate
    if(provider == 'Ria Money Transfer'):
         riarate = rate 

output = output.replace('WU',wurate)
output = output.replace('RIA',riarate)


quote_page = 'https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=INR'
page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
currrate = soup.find('span', attrs={'class': 'uccResultAmount'})
output = output.replace('CURRATE',currrate.text.strip())
# namaj timings 
ts = int(time.time())
response = requests.get("http://api.aladhan.com/v1/timings/"+str(ts)+"?latitude=47.978985&longitude=-122.202079&method=1&latitudeAdjustmentMethod=3")
data = response.json()
fazr = data['data']['timings']['Fajr']
sunrise = data['data']['timings']['Sunrise']
duhr = data['data']['timings']['Dhuhr']
asr = data['data']['timings']['Asr']
magrib = data['data']['timings']['Maghrib']
isha = data['data']['timings']['Isha']
day = data['data']['date']['hijri']["day"]
month = data['data']['date']['hijri']["month"]["en"]
year = data['data']['date']['hijri']["year"]
hizridate = day +" " + month + " "+year
 

fazr = time.strftime( "%I:%M %p", time.strptime(fazr, "%H:%M") )
sunrise = time.strftime( "%I:%M %p", time.strptime(sunrise, "%H:%M") )
duhr = time.strftime( "%I:%M %p", time.strptime(duhr, "%H:%M") )
asr = time.strftime( "%I:%M %p", time.strptime(asr, "%H:%M") )
magrib = time.strftime( "%I:%M %p", time.strptime(magrib, "%H:%M") )
isha = time.strftime( "%I:%M %p", time.strptime(isha, "%H:%M") )

output = output.replace('FAJR',fazr)
output = output.replace('SUNR',sunrise)
output = output.replace('DUHR',duhr)
output = output.replace('ASR',asr)
output = output.replace('MAGRIB',magrib)
output = output.replace('ISHA',isha)
output = output.replace('HIZRA',hizridate)
    
    
# Write output
codecs.open('weather-processed.svg', 'w', encoding='utf-8').write(output)
