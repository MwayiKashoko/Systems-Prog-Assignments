#!/bin/sh

scriptName=$1
directories=`cat $2`

output=`time python3 $scriptName 4 lowbat $directories`
