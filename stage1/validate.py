#!/usr/bin/python
"""
Created by: Shaun Sewell
Student ID: 1234567

Module containing functions to validate input for the forecasting program.

Functions:
    validateInput(args)
    validateDate(date) 
    validateTime(inputTime)
    validateLatLong(lat,lon)
    validatePop(population)
    convertDateAndtimeToUnix(date,inputTime)
    nextWeekDay(date,day) 
"""


#imports
from datetime import datetime
import re
import time


#------------------------------------------------------------------------------------------------

def validateInput(args):
    """
        Validates the input provided in args.
        If args is too small or large raises a value error.
        Returns a list containing the validated lat,lon,pop and forecastTime
    """
    numArgs = len(args)
    if numArgs > 4 and numArgs < 9:
        #retrieve lat and lon
        lat = args[1]
        lon = args[2]
        #validate and store lat and long
        lat,lon = validateLatLong(lat,lon)
        #Retrieve Population
        population = args[3]
        #validate population
        population = validatePop(population)

        #validate date and time
        timeForecast = 0
        if numArgs == 5:        #now
            #validate date
            date = args[4]
            inputDate = validateDate(date)
            #use current system time
            now = datetime.now()
            inputTime = str(now.hour) + ":" + str(now.minute)
            #convert to unix time to use in forecast call
            forecastTime = convertDateAndtimeToUnix(inputDate, inputTime)
        elif numArgs == 6:
            #date and time 
            date = args[4]
            inputTime = args[5]
            #validate date
            inputDate = validateDate(date)
            #validate time
            inputTime = validateTime(inputTime)
            #convert to unix time to use in forecast call
            forecastTime =  convertDateAndtimeToUnix(inputDate, inputTime)
        elif numArgs == 7:
            #date without year and time 
            date = args[4].lower() + " " + args[5].lower()
            inputTime = args[6]
            #validate date
            inputDate = validateDate(date)
            #validate time
            inputTime = validateTime(inputTime)
            #convert to unix time to use in forecast call
            forecastTime =  convertDateAndtimeToUnix(inputDate, inputTime)
        elif numArgs == 8:
            #date without year and time 
            date = args[4].lower() + " " + args[5].lower() + " " + args[6]
            inputTime = args[7].lower()
            #validate date
            inputDate = validateDate(date)
            #validate time
            inputTime = validateTime(inputTime)
            #convert to unix time to use in forecast call
            forecastTime =  convertDateAndtimeToUnix(inputDate, inputTime)
        return [lat,lon,population,forecastTime]
    else:
        if numArgs <= 4:
            raise ValueError('Too few arguments supplied')
        else:
            raise ValueError('Too many arguments supplied')

#------------------------------------------------------------------------------------------------

def validateDate(date):
    """
        Validates the date input is of the form day(alphanumeric) month(alpha) year(optional) or now,day of week
        Returns the date in the format dd/mm/yyyy
        Raises a value error if the date is in the worng format.
    """
    days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday","today","tomorrow","now"]
    alphaMonths = {"january": 31, "february": 28,"march": 31, "april": 30,"may": 31,"june": 30,"july":31,"august":31,"september":31,"october":31,"november":30,"december":31}
    
    if date in days:
        #find next day of week
        if date == "today":
            dateNow = datetime.now()
            return str(dateNow.day) + "/" + str(dateNow.month) + "/" + str(dateNow.year)
            
        elif date == "tomorrow":
            dateNow = datetime.now() + datetime.timedelta(days=1)
            return str(dateNow.day) + "/" + str(dateNow.month) + "/" + str(dateNow.year)
            
        elif date == "now":
            #ignore time
            dateNow = datetime.now()
            return str(dateNow.day) + "/" + str(dateNow.month) + "/" + str(dateNow.year)    
        else:
            #M-S
            dateNow = datetime.now()
            return nextWeekDay(dateNow, date)
    
    else:
        # dd month {yyyy} #alphanumeric
        match = re.search('^(?P<day>\d{1,2})\w{2}\s(?P<month>\w+)\s*(?P<year>\d{4})?',date) 
        if match != None:
            #check if day month combo valid
            day = int(match.group('day'))
            month = match.group('month')
            year = match.group('year')
            
            #check day month year is valid
            if month in alphaMonths:
                numericalMonth = int(datetime.strptime(month ,"%B").month)       #convert month to number
                
                #check if day is valid
                if day > 0 and day <= alphaMonths[month]:
                    #day month valid
                    date = str(day)+"/"+str(numericalMonth)+"/"
                else:    #wrong day for month given
                    raise ValueError('Invalid day ' + str(day) + ' for month ' + month)
                
                if year == None:
                    #use current year
                    dateNow = datetime.now()
                    date += str(dateNow.year)
                else:
                    date += str(year)
                    
                return date
                
            else:        #Invalid month 
                raise ValueError('Invalid month name  ' + month)
        else:
        #not valid
            raise ValueError('Date format is day month {yyyy} not dd/mm/{yyyy}')

#------------------------------------------------------------------------------------------------
  
def validateTime(inputTime):
    """
        Validates the time input is in the form hh:mm(optional)[am|pm] with hours 1-12 and minuntes 0-59.
        Returns time in the 24h format hh:mm
        Raises a value error if the input is in the wrong format
    """
    match = re.search('^(?P<hours>\\d{1,2}):?(?P<minutes>\\d{2})?(?P<AP>am|pm)',inputTime)
    if match != None:
        if match.group('hours') != None and match.group('AP') != None:
            hours = int(match.group('hours'))
            minutes = match.group('minutes')
            if minutes == None:
                minutes = 0
            else:
                minutes = int(minutes)

            AP = match.group('AP')
            if hours > 0 and hours <=12 and minutes >= 0 and minutes <= 59:
                if AP == "pm":
                    hours += 12
                elif AP == "am" and hours == 12:
                    hours = 0
            else:
                if hours < 0 or hours > 12:
                    raise ValueError('Invalid hour input  ' + str(hours) + ', hours must be between 1 and 12.')
                elif minutes < 0 or minutes > 59:
                    raise ValueError('Invalid minute input  ' + str(minutes) + ', minutes must be between 0 and 59.')
                
            return str(hours) +":" + str(minutes)
        else:   
            if match.group('hours') == None:
                raise ValueError('Invalid time input, hours must be between 1 and 12')
            else:
                raise ValueError('Invalid time input, Missing am/pm')
    else:    #use now
        raise ValueError('Invalid time input  ' + inputTime + ', expect 12 hour time with am/pm.')

#------------------------------------------------------------------------------------------------

def validateLatLong(lat,lon):
    """
        Validates that lat and lon are in the format degrees[N|S|E|W]
        Returns the lat and lon as ints.
        lat range 90 to -90 , N is +, S is -
        lon range 180 to -180 E is +, W is -
        Raises a value error if the lat or lon is in the wrong format
    """
    #lat range 90 to -90 , N is +, S is -
    #lon range 180 to -180 E is +, W is -
    latMatch = re.search('^(?P<degrees>\d{1,2})(?P<direction>N|S)',lat)
    if latMatch != None:
        lat = int(latMatch.group('degrees'))
        if lat > -1 and lat < 91:
            if latMatch.group('direction') == "S":
                lat = -lat
        else:
            raise ValueError('Invalid Lattitude ' + str(lat) + ', Lattitude must be between 0 and 90')
    else:
        #raise input error
        raise ValueError('Invalid Lattitude  ' + lat + ', must be between 0 and 90 and include N or S.')

    lonMatch = re.search('^(?P<degrees>\d{1,3})(?P<direction>E|W)',lon)
    if lonMatch != None:
        lon = int(lonMatch.group('degrees'))
        if lon > -1 and lon < 181:
            if lonMatch.group('direction') == "W":
                lon = -lon
        else:
            raise ValueError('Invalid Longitude ' + str(lon) + ', Longitude must be between 0 and 180')
    else:
        raise ValueError('Invalid Longitude  ' + lon + ', must be between 0 and 180 and include E or W.')
        
    return lat,lon
    
#------------------------------------------------------------------------------------------------   

def validatePop(population):
    """
        Validates that the population is in a valid format i.e an integer not a float.
        Returns the validated population.
        Raises a Value Error if the format is wrong.
    """
    #if pop is int 
    try:
        population = int(population)
        return population
    except:
        raise ValueError('Population must be of type int')

#------------------------------------------------------------------------------------------------        
        
def convertDateAndtimeToUnix(date,inputTime):
    """
        Converts the date and time provided into unix time.
        Format for date dd/mm/yyyy
        Format for time hh:mm
        Returns the unix time as an int
    """
    unixTime = time.mktime(datetime.strptime(date+" "+inputTime, "%d/%m/%Y %H:%M").timetuple())
    return int(unixTime)
    
#------------------------------------------------------------------------------------------------
    
def nextWeekDay(date,day):
    """
        Returns the date of the next day.
        Day is from list [monday,tuesday,wednesday,thursday,friday,saturday,sunday]
    """
    #dict to link days of the week to there int representations
    weekdays = {'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6}
    
    #find next day
    dayDiff = weekdays[day] - date.weekday()
    if dayDiff <= 0: # Target day already happened this week
        dayDiff += 7
    return date + datetime.timedelta(dayDiff)
