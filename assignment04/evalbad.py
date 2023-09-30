#!/bin/python3

#importing necessary libraries
import sys
import re

#opening the file that is from the 1st commandline argument
file = open(sys.argv[1], "r")

#number of ip addresses
numIPS=0
#number of domain names
numDomains=0

#the url that shows up the most
highestURL=0
#the count of the url that shows up the most
highestURLCount=0

#unique urls to find out which url shows up the most
uniqueURLS=set()

#determines which lines contain a url that has an ip
for i in file:
    i = i.rstrip()
    #pattern for ip in url
    if re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", i):
        numIPS+=1
        uniqueURLS.add(re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", i)[0])

    #pattern for domain names
    if re.findall("https?://.+\.(com|org|net|co|us)", i):
        numDomains+=1

#determining if the 2nd command line argument exists and if it equals top
if len(sys.argv) > 2 and sys.argv[2] == "top":
    #for loop goes through each element in the uniqueURLS set and compares it in each line of the file to see which url shows up the most
    for IP in uniqueURLS:
        #goes back to the beginning of the file
        file.seek(0)
        count=0
        for line in file:
            line = line.rstrip()

            if re.findall(IP, line):
                count+=1
    
        if count > highestURLCount:
            highestURLCount=count
            highestURL=IP
            
print("Evaluating bad URL file", sys.argv[1])
print("IP Addresses:", numIPS)
print("Domain Names:", numDomains)

if len(sys.argv) > 2 and sys.argv[2] == "top":
    print("Top malicious Site")
    print(highestURL)
    print("Shows up", highestURLCount, "times")

file.close()
print()
