#!/bin/python3
import sys
import os
import json
import re
import functools
import time
import concurrent.futures

#import all functions from analyze
from analyze import *

loadTime = 0
processTime = 0
printTime = 0

jsonFiles = []
beacons = []
selectedBeacons = []
numArr = 0
testList = []

#makes sure command line arguments are correct and able to be parsed
try:
	cores = int(sys.argv[1])
	setting = sys.argv[2]
	directories = sys.argv[3:]

	for i in directories:
		os.scandir(i)
except:
	print("Improper format")
	exit()

if (setting != "lowbat" and setting != "missing" and setting != "missinglow") or len(directories) < 1 or len(directories) > 10:
	print("Improper setting name, or not the right number of directories")
	exit()

for i in directories:
	if not re.search("\d{4}-\d{2}-\d{2}", i):
		exit("Improper directory name format")

#returns the and of each element in the list
def andList(val1, val2):
	return val1 and val2

def loadJSON(directory):
	jsonFiles = []

	for file in os.scandir(directory):
		try:
			jsonFile = open(file)
			jsonFiles.append(json.load(jsonFile))
		except:
			continue

	return jsonFiles

def processBeacons(directories):
	selectedBeacons = []

	newList = []

	i = 0

	while i < len(directories):
		for beacons in directories[i]:
			if setting == "lowbat":
				selectedBeacons = list(map(lowBattery, beacons))
			elif setting == "missing":
				selectedBeacons = list(map(functools.partial(beaconNotSeen, dirName=sys.argv[3+i]), beacons))
			elif setting == "missinglow":
				arr1 = list(map(lowBattery, beacons))
				arr2 = list(map(functools.partial(beaconNotSeen, dirName=sys.argv[3+i]), beacons))
				selectedBeacons = list(map(andList, arr1, arr2))

			for beacon, value in zip(beacons, selectedBeacons):
				if value:
					newList.append(beacon)

		i += 1

	return newList

def printResults(beacon):
	print(beacon["factory_id"])
	print(beacon["name"])
	print(beacon["hardware"])
	print(beacon["battery_level"])
	print(beacon["battery_updated_date"], end="\n\n")

#Only run this code if the name is main so no error
if __name__ == '__main__':
	#use the amount of cores specified
	with concurrent.futures.ProcessPoolExecutor(cores) as executor:
		loadTime1 = time.time()
		jsonFiles = list(executor.map(loadJSON, directories))
		loadTime2 = time.time()

		loadTime = loadTime2 - loadTime1

	with concurrent.futures.ProcessPoolExecutor(cores) as executor:
		processTime1 = time.time()
		selectedBeacons = processBeacons(jsonFiles)
		processTime2 = time.time()

		processTime = processTime2 - processTime1

	with concurrent.futures.ProcessPoolExecutor(cores) as executor:
		printTime1 = time.time()
		executor.map(printResults, selectedBeacons)
		printTime2 = time.time()

		printTime = printTime2 - printTime1

print(loadTime)
print(processTime)
print(printTime)
