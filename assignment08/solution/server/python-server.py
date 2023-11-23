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
    
    if beacon == "" and text.split()[0].lower() == "beacon":
        try:
            for i in jsonFile:
                if text.split()[1] == i["name"]:
                    beacon = i
                    break
        except:
            print("Enter proper beacon name")
            beacon = ""

    #  Send reply back to client
    if text.split()[0].lower() == "beacon" and beacon != "":
        tempString = "0," + beacon["factory_id"] + "," + beacon["name"] + "," + beacon["battery_level"] + "," + beacon["battery_updated_date"] + "," + beacon["hardware"]
        socket.send_string(tempString)
        beacon = ""
    elif text.lower() in beacon:
        res = beacon[text.lower()]
        socket.send_string(res)
    else:
        socket.send_string("FAILURE - IMPROPER INPUT")

    """if text.lower() == "numleft":
        res = jsonFile[name][text.lower()]
        socket.send_string(res)
    elif text.lower() == "factory_id":
        socket.send_string(jsonFile["Send"])
    elif text.lower() == "name":
        pass
    elif text.lower() == "battery_level":
        pass
    elif text.lower() == "battery_updated_date":
        pass
    elif text.lower() == "hardware":
        pass
    else:
        socket.send_string("FAILURE - IMPROPER INPUT")"""
