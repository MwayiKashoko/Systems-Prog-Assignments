# 
#   Go Irish server in Python
#   Binds REP socket to tcp://*:40000
#   Expects b"Go" from client, replies with b"Irish"
#

import time
import zmq
import json
import requests
import re

context = zmq.Context()
socket = context.socket(zmq.REP)

requestURL = "http://ns-mn1.cse.nd.edu/sysprogfa23/assignment08/data/2019-01-21/0.json"
result = None
firstRequest = True

jsonFile = None
hasReceive = True
hasSend = True

beacon = ""
lowbatBeacons = []

# Pick 40000 + last three digits of your 900 ID
serverPort = 40872

try: 
    print('Starting up server on port ' + str(serverPort))
    socket.bind("tcp://*:" + str(serverPort))
except:
    print('Failed to bind on port ' + str(serverPort))
    exit()

while True:
    #  Wait for next request from client
    message = socket.recv()
    print(f"Received request: {message}")

    #  Do some 'work'
    time.sleep(1)

    text = re.findall("'([^']*)'", str(message))[0]
    text = text[0:len(text)-2]

    if firstRequest:
        result = requests.get(requestURL)
        jsonFile = result.json()

        firstRequest = False
    
    #finding the beacon that matches the name
    if text.split()[0] == "beacon":
        try:
            for i in jsonFile:
                if text.split()[1] == i["name"]:
                    beacon = i
                    break
        except:
            print("Enter proper beacon name")
            beacon = ""
    elif text.split()[0] == "id":
        try:
            for i in jsonFile:
                if text.split()[1] == i["id"]:
                    beacon = i
                    break
        except:
            print("Enter proper beacon id")
            beacon = ""

    elif text.split()[0] == "factory_id":
        try:
            for i in jsonFile:
                if text.split()[1] == i["factory_id"]:
                    beacon = i
                    break
        except:
            print("Enter proper beacon factory_id")
            beacon = ""

    elif text == "lowbat":
        #finding all lowbat beacons and adding them to a list
        lowbatBeacons = []
        try:
            for i in jsonFile:
                if "low" in i["battery_level"].lower():
                    lowbatBeacons.append(i)
        except:
            print("ERROR")
            lowbatBeacons = []
    elif "http://ns-mn1.cse.nd.edu/sysprogfa23/assignment08/data/" in text:
        requestURL = text
        result = requests.get(requestURL)
        jsonFile = result.json()
        socket.send_string("Changed files")
        continue

    #  Send reply back to client
    if (text.split()[0] == "beacon" or text.split()[0] == "id" or text.split()[0] == "factory_id") and beacon != "":
        num = int(beacon["id"], 16)
        tempString = "0," + beacon["factory_id"] + "," + beacon["name"] + "," + beacon["battery_level"] + "," + beacon["battery_updated_date"] + "," + beacon["hardware"] + "," + beacon["id"] + "," + str(num)
        socket.send_string(tempString)
        beacon = ""
    elif (text == "lowbat" or text == "more")  and len(lowbatBeacons) > 0:
        num = int(lowbatBeacons[0]["id"], 16)
        tempString = str(len(lowbatBeacons)-1) + "," + lowbatBeacons[0]["factory_id"] + "," + lowbatBeacons[0]["name"] + "," + lowbatBeacons[0]["battery_level"] + "," + lowbatBeacons[0]["battery_updated_date"] + "," + lowbatBeacons[0]["hardware"] + "," + lowbatBeacons[0]["id"] + "," + str(num)
        socket.send_string(tempString)
        lowbatBeacons.pop(0)
    else:
        socket.send_string("FAILURE - IMPROPER INPUT")
