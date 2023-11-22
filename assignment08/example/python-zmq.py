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

requestURL1 = "http://ns-mn1.cse.nd.edu/sysprogfa23/assignment08/test/data.json"
requestURL2 = "http://ns-mn1.cse.nd.edu/sysprogfa23/assignment08/test/data-switch.json"
currURL = requestURL1
result = None
firstRequest = True

jsonFile = None
hasReceive = True
hasSend = True

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

    if firstRequest:
        result = requests.get(requestURL1)
        jsonFile = result.json()

        firstRequest = False

    text = re.findall("'([^']*)'", str(message))[0]
    text = text[0:len(text)-2]

    print(text)

    if "switch" == text.lower():
        if currURL == requestURL1:
            currURL = requestURL2
        else:
             currURL = requestURL1

        result = requests.get(currURL)
        jsonFile = result.json()

    if not jsonFile["Receive"].upper() == str(text).upper():
        hasReceive = False
    else:
         hasReceive = True

    if not jsonFile["Send"].upper() == str(text).upper():
        hasSend = False
    else:
        hasSend = True

    #  Send reply back to client
    if hasReceive:
        socket.send_string(jsonFile["Receive"])
    elif hasSend:
        socket.send_string(jsonFile["Send"])
    elif "switch" == text.lower():
        socket.send_string("switch")
    else:
        temp = "Error - Wrong Text - Expected " + jsonFile["Receive"]
        socket.send_string(temp)
