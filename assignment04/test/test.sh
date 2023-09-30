#!/bin/sh

compiler=0

if [ "$1" = "../evalbad.sh" ]; then
  compiler="sh"
elif [ "$1" = "../evalbad.py" ]; then
  compiler="python3"
else
  echo That is not a valid program
  exit 1
fi

#1st test case (correct file 20 urls)
$compiler $1 ../BadURL-First20.csv

#2nd test case (incorrect file name)
$compiler $1 ../BadURL-Fi

#3rd test case (correct file 20 urls top)
$compiler $1 ../BadURL-First20.csv top

#4th test case (empty file)
$compiler $1 empty.csv

#5th test case (corrupted file 20 urls top 10% corrupted)
$compiler $1 corrupted20urls.csv top
