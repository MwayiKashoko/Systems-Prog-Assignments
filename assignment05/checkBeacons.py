#!/bin/python3
import sys
import json
import os
import re

numJSONFiles = 0
numBeacons = 0

lowBat = len(sys.argv) == 3 and sys.argv[2] == "-lowbat"

try:
    os.scandir(sys.argv[1])
except:
    print("Either no argument given or incorrect directory name")
    exit()

for f in os.scandir(sys.argv[1]):
    if re.search("(\.json)$", f.name):
        numJSONFiles += 1

        loadFile=open(sys.argv[1] + "/" + f.name)

        try:
            jsonFile=json.load(loadFile)
        except:
            continue
        
        for i in jsonFile:
            if lowBat:
                if "Low" in i.values():
                    print(i["factory_id"] + "," + i["name"] + "," + i["hardware"] + "," + i["battery_level"] + "," + i["battery_updated_date"], end="\n")
                    numBeacons += 1
            else:
                print(i["factory_id"])
                print(i["name"])
                print(i["hardware"])
                print(i["battery_level"])
                print(i["battery_updated_date"], end="\n\n")
                numBeacons += 1

        loadFile.close()

if lowBat:
    print("There are", numJSONFiles, "JSON Files and", numBeacons, "low battery beacons.")
else:
    print("There are", numJSONFiles, "JSON Files and", numBeacons, "total beacons.")
