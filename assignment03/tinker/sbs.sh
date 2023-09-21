#!/bin/sh

#$1 is the list of bad sites which is going to be used to check if $2 is malicious

#cat command outputs the text of the file to stdout, and then grep looks for ALL urls in the stdout, after this it makes sure that each file in unique
BadFiles=`cat $1 | grep -Eo "(http|https)://[a-zA-Z0-9./?=_%:-]*" | uniq`

#The BadFiles variable is currently separated by spaces for each URL, but the for loop does not like this so i convert every space character to a new line
BadFiles=$(echo "$BadFiles" | tr [:space:]' '\n')

IsClean=true

#read through each line of BadFiles
for i in $BadFiles; do
  #Basically if the url has https://urlhaus.abuse.ch/ in it, we know it is safe and is not malicious so we want to ignore those urls
  if ! `echo $i | grep -q "https://urlhaus.abuse.ch/"`; then
    if `cat $2 | grep -Eoq "$i"`; then
      echo MALWARE SPOTTED
      echo MALICIOUSURL: $i
      IsClean=false
    fi
  fi
done

#if everything is clean then echo that the email is clean
if $IsClean; then
  echo CLEAN
fi
