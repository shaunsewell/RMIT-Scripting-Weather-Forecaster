#!/usr/bin/python
"""
Created by: Shaun Sewell
Student ID: 1234567

Module containing functions to handle processing of the world cities file.

Functions:
    getDistance(latitude1,longitude1,latitude2,longitude2)
    findCitiesAbovePop(population,cities)
    findNearestCities(latitude,longitude,cities,numCities)
    loadCities()
    cacheCities(cities)
    
"""

__author__ = "Shaun Sewell"

#imports
from math import sin,cos,acos,atan2,sqrt,radians,asin
import csv
import sys
from operator import itemgetter



def getDistance(latitude1,longitude1,latitude2,longitude2):
    """
        Returns the Great Circle Distance in Km between two locations represented as lat,lon pairs.
        Latitude and Longitude must be in degrees
        Uses the Spherical law of cosines.
        Formula obtained from https://en.wikipedia.org/wiki/Great-circle_distance.
    """
    radius = 6371 #mean earth radius in km
    sinPart = sin(radians(latitude1))*sin(radians(latitude2))
    cosPart = cos(radians(latitude1))*cos(radians(latitude2))*cos(abs(radians(longitude2) - radians(longitude1)))
    distance = radius*acos(sinPart+cosPart)
    return distance

#--------------------------------

def findCitiesAbovePop(population,cities):
    """
        Returns a list of cities with a pop equal or greater than population.
        Supplied cities list is assumed to be sorted in ascending order.
    """
    for city in cities:
        if city[1] >= population:
            #split cities at index of city
            return cities[cities.index(city):]

#--------------------------------            
    
def findNearestCities(latitude,longitude,cities,numCities):
    """
        Returns a list of the closest cities to latitude,longitude.
        The returned list is of length numCities.
    """
    distanceToNearest = 1000000 #impossible distance to have on earth
    nearestCity = []
    for city in cities:
        distance = getDistance(latitude, longitude, float(city[2]), float(city[3]))
        if distance < distanceToNearest:
            city.append(distance)            #add distance to city
            nearestCity.append(city)         #add to list of cities 
            distanceToNearest = distance
            
    nearestCity.sort(key=lambda x:x[4])    #sort list by distance
    return nearestCity[:numCities]
    
#--------------------------------

def loadCities():
    """
        Returns a list of cities sorted by population.
        Cities are read from either cache.txt or worldcities.txt 
        Cache.txt contains a list of cities sorted by population with the empty entries removed.
        Format of worldcities entries Country,City,AccentCity,Region,Population,Latitude,Longitude
    """
    
    #list to store cities in
    data = []
    
    #try opening cache
    try:
        fileReader = csv.reader(open("world_cities/cache.txt",'r'))
        for row in fileReader:
            data.append(row)
        return data
    except:
        try:
            fileReader = csv.reader(open("world_cities/worldcitiespop.txt",'r'))
            #remove column headers
            fileReader.next()
            for row in fileReader:
                if row[4] != '':
                    row[4] = int(row[4])            #population
                    row[5] = float(row[5])          #latitude
                    row[6] = float(row[6])          #longitude
                    cityEntry = [row[1],row[4],row[5],row[6]]        #row[1] is the city name
                    data.append(cityEntry)

            sortedList = sorted(data,key=lambda x: x[1])
            cacheCities(sortedList)
            return sortedList
        except Exception as e:
            raise e

#--------------------------------

def cacheCities(cities):
    """
        Writes the sorted list of cities to cache.txt.
    """
    try:
        with open('world_cities/cache.txt', 'w') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerows(cities)
    except Exception as e:
        raise e


#--------------------------------   