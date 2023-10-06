#!/bin/python
#importing necessary libraries
import sys
import json

#Making sure that the user input is correct (makes sure file exists, and that there is enough aruguments) otherwise the program stops
try:
    f=open(sys.argv[1])
except:
    print("File is non-existant or not enough arguments")
    exit()

#If the file cannot be parsed then stop the program
try:
    jsonFile = json.load(f)
except:
    print("File can't be parsed")
    exit()

#Total number of beacons in the file
numBeacons = 0

for data in jsonFile:
    print(data["factory_id"])
    print(data["name"])
    print(data["hardware"])
    print(data["battery_level"])
    print(data["battery_updated_date"], end="\n\n")
    
    numBeacons += 1

print("Total number of beacons:", numBeacons)

f.close()
