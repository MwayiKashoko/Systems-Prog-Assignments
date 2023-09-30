#!/bin/sh

#Getting the 1st command line argument and setting it as the variable name file
File=$1

#Tests if the file exists. If it does then the program will run
if ! [ -e $File ]; then
  echo FILE DOES NOT EXIST
  printf "\n"
  exit 1
fi

echo "Evaluating bad URL file $File"

#UniqueIPS regex determines all the cases where an IP address occurs in a url and stores it uniquely
#AllIPS gets all IPs
#NumIPS returns the number of IPS
#NumDomainNames returns num of domain names ending in com|org|net|co|us
#HighestURL the url that occurs the most often
#HighestURLCount the count of the highest URL

UniqueIPS=`cat $File | grep -Eo "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" | sort -u`
AllIPS=`cat $File | grep -Eo "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"`
NumIPS=`cat $File | grep -Eoc "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"`
NumDomainNames=`cat $File | grep -Eoc "https?://.+\.(com|org|net|co|us)"`
HighestURL=0
HighestURLCount=0

#if the 2nd argument = top then we will find the highest url through a nested for loop that goes through each line of UniqueIPS and AllIPS to find all the matches
if [ "$2" = top ]; then
  for IP in $UniqueIPS; do
    count=0
    for line in $AllIPS; do
      #if the ip is a match for the line count++
      if echo $line | grep -Eoq $IP; then
        count=$((count+1))
      fi
    done

    #if count is greater that the current highesturlcount we have a new highesturlcount
    if [ $count -gt $HighestURLCount ]; then
      HighestURLCount=$count
      HighestURL=$IP
    fi
  done
fi

echo "IP Adresses: $NumIPS"
echo "Domain Names: $NumDomainNames"

if [ "$2" = top ]; then
  printf "\n"
  echo "Top Malicious Site"
  echo "$HighestURL"
  echo "shows up $HighestURLCount times"
fi

printf "\n"
