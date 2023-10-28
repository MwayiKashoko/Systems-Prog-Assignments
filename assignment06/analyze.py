import re
import datetime

#Checks to see if it is possible to make a date
def isDate(var):
    return re.search("\d+-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z", var)

#Calculates the days between date1 and date2 making sure to account for negative values
def calculateDays(date1, date2):
    dateNum = int(re.search("\d+", str(date1-date2))[0])

    return dateNum

#parse date to make it into a date object
def parseDate(var):
    year = int(var[:4])
    month = int(var[5:7])
    day = int(var[8:10])

    return datetime.datetime(year, month, day)

#Determine if a beacon has a low battery
def lowBattery(beacon):
	if re.search("low", beacon["battery_level"].lower()):
		return True

	return False

#Determines if a beacon has not been seen after 7 days from the directory name
def beaconNotSeen(beacon, dirName):
	beaconDate = beacon["battery_updated_date"]
	dirDate = datetime.datetime(int(dirName[:4]), int(dirName[5:7]), int(dirName[8:10]))

	if beaconDate != None and isDate(beaconDate) and calculateDays(dirDate, parseDate(beaconDate)) > 7:
		return True

	return False#!/bin/python3
