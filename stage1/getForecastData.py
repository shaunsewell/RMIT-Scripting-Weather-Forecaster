#!/usr/bin/python
"""
Created by: ?
Modified by: Shaun Sewell
Student ID: 1234567

Module for requesting a weather forecast.

Functions:
	getForecast(url,apikey,latitude,longitude,options)
"""

#imports
import httplib		# so we can make a call to the service
import json			# so we can decode the response

#-------------------
def getForecast(url, apikey, latitude, longitude, options):
	"""
		Attempts to request a forecast from forecast.io
		Returns the data obtained as well as a response code.
	"""
	try:
		
		connection = httplib.HTTPSConnection(url)
		path = "/forecast/" + apikey + "/" + latitude + "," + longitude  + options
		
		connection.request("GET", path)

		response = connection.getresponse()
		
		#Test if request succeeded
		if response.status == 200: #success
			data = response.read()
			return json.loads(data),response.status 
		else: #Failure
			return None,response.status
	except Exception as e:
		raise e
#-------------------
	

