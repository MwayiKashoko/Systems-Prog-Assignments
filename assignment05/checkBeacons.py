#!/bin/python3
#Importing necessary libraries
import sys
import json
import os
import re
import datetime

#total number of json files and beacons
numJSONFiles = 0
numBeacons = 0

#Checks to see if lowbat and notseen are present and in place correctly
lowBat = (len(sys.argv) == 3 and sys.argv[2] == "-lowbat") or (len(sys.argv) == 6 and sys.argv[2] == "-lowbat")
notSeen = (len(sys.argv) == 5 and sys.argv[2] == "-notseen") or (len(sys.argv) == 6 and sys.argv[3] == "-notseen")

#Returns whether or not a variable is an integer
def isInt(var):
    return type(var) == int

#If the input is in the specified format for a date then return true
def isDate(var):
    return re.search("\d+-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z", var)

#Calculates the days between date1 and date2 making sure to account for negative values
def calculateDays(date1, date2):
    dateNum = int(re.search("\d+", str(date1-date2))[0])

    if date2 > date1:
        dateNum *= -1

    return dateNum

#parse date to make it into a date object
def parseDate(var):
    year = int(var[:4])
    month = int(var[5:7])
    day = int(var[8:10])
    hour = int(var[11:13])
    minute = int(var[14:16])
    second = int(var[17:19])
    millisecond = int(var[20:23])

    return datetime.datetime(year, month, day, hour, minute, second, millisecond*1000)

#If the -notseen flag is present then run these tests to make sure all of the variables are placed correctly in order to make the code run effectively
if notSeen:
    if len(sys.argv) == 5:
        try:
            #checks if the 4th argument (N) is an integer and exits if not
            int(sys.argv[3])

            #Checks if the 5th argument (DATE) is a valid date and exits if not
            if not isDate(sys.argv[4]):
                print("ERROR: Not valid syntax for the data which is XXXX-XX-XXTXX:XX:XX.XXXZ Replace X with numbers (Year, Month, Day, Hour, Minute, Second, Milliseconds)")
                exit()
        except:
            print("ERROR: Have to enter an integer after the -notseen flag")
            exit()

        currentDate = parseDate(sys.argv[4])
        #numDays that have to have been passed to show the file
        numDays = int(sys.argv[3])
    elif len(sys.argv) == 6:
        #same logic as the previous chunk just incremented one more to account for the -lowbat flag
        try:
            int(sys.argv[4])

            if not isDate(sys.argv[5]):
                print("ERROR: Not valid syntax for the data which is XXXX-XX-XXTXX:XX:XX.XXXZ Replace X with numbers (Year, Month, Day, Hour, Minute, Second, Milliseconds)")
                exit()
        except:
            print("ERROR: Have to enter an integer after the -notseen flag")
            exit()

        currentDate = parseDate(sys.argv[5])
        numDays = int(sys.argv[4])

#if this dir exists then continue, else exit the program
try:
    os.scandir(sys.argv[1])
except:
    print("Either no argument given or incorrect directory name")
    exit()

#If the -notseen flag is present then add some extra spaces before produce the output
if notSeen:
    print(end="\n\n\n\n\n\n\n\n\n\n")

#Going through each file in the directory
for f in os.scandir(sys.argv[1]):
    #Checking the end of the name to see if it is a json file
    if re.search("(\.json)$", f.name):
        numJSONFiles += 1

        #Have to account for the path when opening a file
        loadFile=open(sys.argv[1] + "/" + f.name)

        #If the json file is valid, then run the code, else move onto the next one
        try:
            jsonFile=json.load(loadFile)
        except:
            numJSONFiles -= 1
            continue
        
        #Now going through each beacon in each JSON file
        for i in jsonFile:
            #If it is true then display the beacon
            canDisplay = True
            #battery_updated_date of each beacon
            beaconDate = i["battery_updated_date"]

            #checking to make sure that there is a date for the beacon if -notseen is present
            if notSeen and isDate(str(beaconDate)):
                #The actual date of the file in python readable format
                fileDate = parseDate(beaconDate)

                #If the number of days prior to the currentDate is less than the number of days inputted, then don't display the file
                if calculateDays(currentDate, fileDate) < numDays:
                    canDisplay = False

            if canDisplay:
                if lowBat:
                    if "Low" in i.values():
                        #Displays in CSV friendly format if -lowbat
                        print(i["factory_id"] + "," + i["name"] + "," + i["hardware"] + "," + i["battery_level"] + "," + beaconDate, end="\n")
                        numBeacons += 1
                else:
                    #Normal display if no -lowbat
                    print(i["factory_id"])
                    print(i["name"])
                    print(i["hardware"])
                    print(i["battery_level"])
                    print(beaconDate, end="\n\n")

                    numBeacons += 1

        loadFile.close()

if lowBat:
    print("There are", numJSONFiles, "JSON Files and", numBeacons, "low battery beacons.")
else:
    print("There are", numJSONFiles, "JSON Files and", numBeacons, "total beacons.")
