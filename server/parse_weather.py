
import urllib3
from xml.dom import minidom
import datetime
import codecs
import sys
import requests
import time
import json
import traceback
import pytz
#from datetime import datetime

# exchange rate
# chage
if sys.version_info[0] == 3:
    from urllib.request import urlopen
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlopen

from bs4 import BeautifulSoup


def getDollarExchangeRates():
  remitly = "Err"
  xoom = "Err"
  wurate = "Err"
  riarate ="Err"
  currrate ="Err"
  # get remitily and xoom data from remetly website
  try:
      quote_page = 'https://www.remitly.com/us/en/india'
      page = urlopen(quote_page)
      soup = BeautifulSoup(page, 'html.parser')
      remitly_box = soup.findAll('span', attrs={'class': 'remitly-rate'})[1]
      xoom_box = soup.findAll('span', attrs={'class': 'competitor-rate'})[0]
      remitly = remitly_box.text.strip()
      xoom = xoom_box.text.strip()
      
  except:
     print("error with remitly conversion");      
  
  #get western union and ria data from entry india website
  try:
      quote_page = 'http://entryindia.com/exchange_rates'
      page = urlopen(quote_page)
      soup = BeautifulSoup(page, 'html.parser')
      tbody = soup.findAll('tbody', attrs={'id': 'ei_bxr_table'})[0]
      trs = tbody.findAll('tr')
      #wurate = 0
      #riarate = 0
      for tr in trs:
    
          provider = tr.findAll('td')[0].find('p').text.strip()
          rate = tr.findAll('td')[1].text.strip().rstrip('Fixed').rstrip('Indicativ')
          if(provider == 'Western Union'):
              wurate = rate
          if(provider == 'Ria Money Transfer'):
              riarate = rate 

  except:
      print("error entry india exchange")

  print("Getting currency convert")
  try:    
      with urlopen("http://free.currencyconverterapi.com/api/v5/convert?q=USD_INR&compact=y") as url:
          data = json.loads(url.read().decode())
          print(data)
          currrate = str(data['USD_INR']['val'])
          print(currrate)
  except ValueError:
      print("error with currency covert api "+ ValueError)
      
  return {'remitly':remitly, 'xoom':xoom, 'wurate':wurate, 'riarate':riarate,'currrate':currrate }

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


def getISTTime():
        intz = pytz.timezone('Asia/Kolkata')
        nowdt = datetime.datetime.now(intz)
        return nowdt


def getWeatherForcast():
	#return '{"location":{"woeid":2367188,"city":"Bothell","region":" WA","country":"United States","lat":47.77388,"long":-122.203812,"timezone_id":"America/Los_Angeles"},"current_observation":{"wind":{"chill":21,"direction":350,"speed":8.08},"atmosphere":{"humidity":67,"visibility":10.0,"pressure":29.5,"rising":0},"astronomy":{"sunrise":"7:25 am","sunset":"5:22 pm"},"condition":{"text":"Mostly Cloudy","code":28,"temperature":29},"pubDate":1549760400},"forecasts":[{"day":"Sat","date":1549699200,"low":24,"high":31,"text":"Snow","code":16},{"day":"Sun","date":1549785600,"low":11,"high":32,"text":"Partly Cloudy","code":30},{"day":"Mon","date":1549872000,"low":24,"high":34,"text":"Rain And Snow","code":5},{"day":"Tue","date":1549958400,"low":30,"high":38,"text":"Rain And Snow","code":5},{"day":"Wed","date":1550044800,"low":24,"high":36,"text":"Partly Cloudy","code":30},{"day":"Thu","date":1550131200,"low":18,"high":38,"text":"Rain And Snow","code":5},{"day":"Fri","date":1550217600,"low":31,"high":39,"text":"Rain And Snow","code":5},{"day":"Sat","date":1550304000,"low":30,"high":37,"text":"Rain And Snow","code":5},{"day":"Sun","date":1550390400,"low":25,"high":34,"text":"Rain And Snow","code":5},{"day":"Mon","date":1550476800,"low":22,"high":34,"text":"Mostly Cloudy","code":28}]}'
	f = open("yahooapi_response", "r")
	return f.read()


output = codecs.open('template.svg', 'r', encoding='utf-8').read()
try:
	#Code of my city
	isttime = getISTTime().strftime("%I:%M %p")
	istweekday = getISTTime().strftime("(%A - %m/%d)")
	#print(isttime)
	#output = output.replace('IST',isttime)
	METRIC = True
	weatherResponse = getWeatherForcast()
	weatherJSON =  json.loads(weatherResponse)
	status = weatherJSON["forecasts"][0]["text"]
	image = weatherJSON["forecasts"][0]["code"]
	date = weatherJSON["forecasts"][0]["date"]
	#output = output.replace('As of TIME',datetime.fromtimestamp(date).strftime('%m-%d'))

	#can't trust windchill if specified in celsius (must parse from fahrenheit)
	#concisedates = date.split()
	#concisedate = ' '.join([concisedates[2],concisedates[1].lstrip("0")])
	#concisetime = ' '.join([concisedates[4],concisedates[5]])
	#concisetime = concisetime + ' ('+concisedates[0].rstrip(",")+')';
	temp = weatherJSON["current_observation"]["condition"]["temperature"]
	low = weatherJSON["forecasts"][0]["low"]
	high =weatherJSON["forecasts"][0]["high"]

	future1low = weatherJSON["forecasts"][1]["low"]
	future1high = weatherJSON["forecasts"][1]["high"]
	future1day = weatherJSON["forecasts"][1]["day"]

	future2low =  weatherJSON["forecasts"][2]["low"]
	future2high =  weatherJSON["forecasts"][2]["high"]
	future2day =  weatherJSON["forecasts"][2]["day"]

	future3low =  weatherJSON["forecasts"][3]["low"]
	future3high =  weatherJSON["forecasts"][3]["high"]
	future3day =  weatherJSON["forecasts"][3]["day"]

	future4low =  weatherJSON["forecasts"][4]["low"]
	future4high =  weatherJSON["forecasts"][4]["high"]
	future4day =  weatherJSON["forecasts"][4]["day"]


	chill = weatherJSON["current_observation"]["wind"]["chill"]
	direction = weatherJSON["current_observation"]["wind"]["direction"]
	speed = weatherJSON["current_observation"]["wind"]["speed"]
	humidity = weatherJSON["current_observation"]["atmosphere"]["humidity"]
	pressure = weatherJSON["current_observation"]["atmosphere"]["pressure"]
	#pressureunit = weatherJSON["current_observation"]["atmosphere"]["humidity"]
	city = weatherJSON["location"]["city"]
	sunset = weatherJSON["current_observation"]["astronomy"]["sunset"]
	sunrise = weatherJSON["current_observation"]["astronomy"]["sunrise"]
	image_url = 'assets/' + str(image) + '.png'
	f1image_url = 'assets/' +  str(weatherJSON["forecasts"][1]["code"]) + '.png'
	f2image_url = 'assets/' + str(weatherJSON["forecasts"][2]["code"]) + '.png'
	f3image_url = 'assets/' + str(weatherJSON["forecasts"][3]["code"]) + '.png'
	f4image_url = 'assets/' + str(weatherJSON["forecasts"][4]["code"]) + '.png'
	# Open SVG to process
	output = codecs.open('template.svg', 'r', encoding='utf-8').read()

	# Insert icons and temperatures
	#output = output.replace('TODAY',concisedate)
	#output = output.replace('TIME',concisetime)
	#print(humidity)
	output = output.replace('As of TIME',datetime.datetime.fromtimestamp(date).strftime('%A'))
	output = output.replace('IST',isttime)
	output = output.replace('IND_WKDAY',istweekday)
	output = output.replace('CITY',city)
	output = output.replace('HUMID',str(humidity))
	output = output.replace('ICON_ONE',image_url)
	output = output.replace('HIGH_ONE',str(high))

	output = output.replace('F1',future1day+":"+str(future1low)+"/"+str(future1high))
	output = output.replace('F2',future2day+":"+str(future2low)+"/"+str(future2high))
	output = output.replace('F3',future3day+":"+str(future3low)+"/"+str(future3high))
	output = output.replace('F4',future4day+":"+str(future4low)+"/"+str(future4high))
	output = output.replace('ICON_FU1',f1image_url)
	output = output.replace('ICON_FU2',f2image_url)
	output = output.replace('ICON_FU3',f3image_url)
	output = output.replace('ICON_FU4',f4image_url)


	output = output.replace('CURR_TEMP',str(temp))
	output = output.replace('LOW_ONE',str(low))
	output = output.replace('SUNSET',sunset.rstrip(' pm'))
	output = output.replace('SUNRISE',sunrise.rstrip(' am'))

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
except Exception:
	traceback.print_exc()
	output = output.replace('CITY','Bothell')  
	

monthmap = ["Jan", "Feb", "March", "April", "May", "June", "July","Aug","Sep","Oct","Nov","Dec"]
output = output.replace('TODAY', monthmap[datetime.date.today().month - 1] + ' '+str(datetime.date.today().day)) 
exchangeRates  = getDollarExchangeRates()
print(exchangeRates)
output = output.replace('REMITLY',exchangeRates['remitly'])
output = output.replace('XOOM',exchangeRates['xoom'])
output = output.replace('WU',exchangeRates['wurate'])
output = output.replace('RIA',exchangeRates['riarate'])
output = output.replace('CURRATE',exchangeRates['currrate'])     



# namaj timings 
ts = int(time.time())
# adding one day to fix the offset of the api
ts = ts +(24*60*60)
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
 

fazr = time.strftime( "%I:%M", time.strptime(fazr, "%H:%M") )
sunrise = time.strftime( "%I:%M", time.strptime(sunrise, "%H:%M") )
duhr = time.strftime( "%I:%M", time.strptime(duhr, "%H:%M") )
asr = time.strftime( "%I:%M", time.strptime(asr, "%H:%M") )
magrib = time.strftime( "%I:%M", time.strptime(magrib, "%H:%M") )
isha = time.strftime( "%I:%M", time.strptime(isha, "%H:%M") )

output = output.replace('FAJR',fazr)
output = output.replace('SUNR',sunrise)
output = output.replace('DUHR',duhr)
output = output.replace('ASR',asr)
output = output.replace('MAGRIB',magrib)
output = output.replace('ISHA',isha)
output = output.replace('HIZRA',hizridate)
    
    
# Write output
codecs.open('weather-processed.svg', 'w', encoding='utf-8').write(output)


	

