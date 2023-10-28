#!/bin/sh

scriptName=$1
directories=`cat $2`

#Outputs only the time that it takes to run the script
output=`time python3 $scriptName 4 lowbat $directories`
