#!/usr/bin/python
"""
Created by: Shaun Sewell
Student ID: 1234567

Module for building webpages

Functions:
	createWebFormPage()
	respondToSubmit(parameters) 
	
"""

#imports
import cgi
from getLocationFromIP import getLocation
from getForecastData import getForecast
import city
import time

#----------------------------------------------------------------
def createWebFormPage():
	"""
		Main webpage. 
		Request location of the device and displays a list of the 10 nearest cities to request a forecast for.
	"""
	locationData,responseCode = getLocation()
	
	if responseCode == 200:	#call was successful
		cities = city.loadCities()
		#lat lon from data
		#find 10 nearest cities
		nearestCities = city.findNearestCities(locationData['latitude'], locationData['longitude'], cities, 10)
		#display list of options
		data = "<html><head><title>Demonstration of a webserver</title></head><body>\n"
		data += '<form action="http://localhost:34567/" method="POST">\n'
		data += '<select name="location">'
		for element in nearestCities:
			data += '<option value="'+ str(element[2]) + ',' + str(element[3]) + '">' + str(element[0]) + '</option>'
		data += '</select>'
		data += '<input type="submit" id="submit"></submit>'
		data += '</form>'
		data += '</body></html>\n'		
		return data
	else: 	#Location call unsuccessful
		data = "<html><head><title>Demonstration of a webserver</title></head><body>\n"
		data += "Failed to get location<br>" 
		data += "Error" + responseCode + "<br>" 
		data += '</body></html>\n'		


#----------------------------------------------------------------

def respondToSubmit(parameters):
	"""
		Response page.
		Gathers a forecast for the chosen city 
	"""
	APIKEY = "null"  #key for forecast.io 		
	location = parameters['location']
	lat,lon = location.split(',')
	forecastTime = int(time.time())
	
	currentForecast,responseCode = getForecast("api.forecast.io", APIKEY, str(lat), str(lon), ","+str(forecastTime)+"?exclude=hourly,minutely,daily,alerts,flags&units=si")
	
	if responseCode == 200:
		print 
		data = "<html><head><title>Demonstration of a webserver</title></head><body>\n"
		data += "Timezone: " + currentForecast['timezone']+ "<br>" 
		currentForecast = currentForecast['currently']
		data += "Temperature: " + str(currentForecast['temperature'])+"C<br>" 
		data += "Summary: " + str(currentForecast['summary']) + "<br>"
		data += "Humidity: " + str(currentForecast['humidity']*100)+"%<br>"
		data += "Wind Speed: " + str(currentForecast['windSpeed'])+"m/s<br>"
		data += "<a href=""https://darksky.net/poweredby""/>Powered by Dark Sky</a><br>"
		data += '</body></html>\n'		
		return data
	else:
		data = "<html><head><title>Demonstration of a webserver</title></head><body>\n"
		data += "Failed to obtain a forecast<br>" 
		data += "Error" + responseCode + "<br>" 
		data += '</body></html>\n'		
