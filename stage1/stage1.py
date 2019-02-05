#!/usr/bin/python
"""
Created by: Shaun Sewell
Student ID: 1234567

Main program.
Use arguments provided at runtime to forecast the weather.
"""

#imports
import sys
from validate import *
import city
import datetime
from getForecastData import getForecast
import time

if __name__ == "__main__":
    sys.tracebacklimit = 0
    APIKEY = "null"  #key for forecast.io
    
    #validate input
    lat,lon,population,forecastTime = validateInput(sys.argv)

    #initialise cities
    cities = city.loadCities()
    #find city nearest lat,lon with population above population
    popAdjustedCities = city.findCitiesAbovePop(population, cities)
    closestCity = city.findNearestCities(lat, lon, popAdjustedCities, 1)[0]
    
    #create forecast request
    currentForecast,responseCode = getForecast("api.forecast.io", APIKEY, str(closestCity[2]), str(closestCity[3]), ","+str(forecastTime)+"?exclude=hourly,minutely,daily,alerts,flags&units=si")
    if currentForecast != None:
        #Display important details
        #timezone temperature,summary, humidity, windspeed
        print "Timezone: " + currentForecast['timezone']
        currentForecast = currentForecast['currently']
        print "Temperature: " + str(currentForecast['temperature'])+"C" 
        print "Summary: " + str(currentForecast['summary'])
        print "Humidity: " + str(currentForecast['humidity']*100)+"%"
        print "Wind Speed: " + str(currentForecast['windSpeed'])+"m/s"
        print "Powered by Dark Sky - https://darksky.net/poweredby/"
    else:
        print "Failed to get forecast."
        print "Error " + str(responseCode)
        
    