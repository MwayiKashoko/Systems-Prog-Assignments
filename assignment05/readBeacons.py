#!/bin/python
import sys
import json

try:
    f=open(sys.argv[1])
except:
    print("File is non-existant or not enough arguments")
    exit()

jsonFile = json.load(f)

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
