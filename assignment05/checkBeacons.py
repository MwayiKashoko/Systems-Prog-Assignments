#!/bin/python3
import sys
import json
import os
import re

numJSONFiles = 0
numBeacons = 0

for f in os.scandir(sys.argv[1]):
    if re.search("(\.json)$", f.name):
        numJSONFiles += 1

        loadFile=open(f.name)
        jsonFile=json.load(loadFile)
        
        for i in jsonFile:
            if len(sys.argv) == 3 and sys.argv[2] == "-lowbat":
                print(i["factory_id"] + "," + i["name"] + "," + i["hardware"] + "," + i["battery_level"] + "," + i["battery_updated_date"], end="\n")
            else:
                print(i["factory_id"])
                print(i["name"])
                print(i["hardware"])
                print(i["battery_level"])
                print(i["battery_updated_date"], end="\n\n")

            numBeacons += 1

print("There are", numJSONFiles, "JSON Files and", numBeacons, "beacons.")
