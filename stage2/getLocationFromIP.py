#!/usr/bin/python
"""
Created by: Shaun Sewell
Student ID: 1234567

Module for requesting device location based on IP address.

Functions:
    getLocation()
"""
#imports
import httplib		# so we can make a call to the service
import json			# so we can decode the response

#----------------------------------------------------------------
def getLocation():
    """
        Attempts to obtain a location from freegeoip.net
        Returns the data obtained as well as a response code.
    """
    try:
        connection = httplib.HTTPConnection("freegeoip.net")
        connection.request("GET", "/json/")
        
        response = connection.getresponse()
        #Test if request succeeded
        if response.status == 200: #success
            data = response.read()
            return json.loads(data),response.status 
        else: #Failure
            return None,response.status

    except Exception as e:
        raise e
#----------------------------------------------------------------   

