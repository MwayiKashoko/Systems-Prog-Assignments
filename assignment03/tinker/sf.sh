#!/bin/sh

#finding all instances of a SSN
SSN=`cat $1 | grep -Eo "[0-9]{3}-[0-9]{2}-[0-9]{4}"`

#Gets the length of the SSN string
length=${#SSN}

hasSSN=false
hasSensitive=false
isClean=true

#if the length of SSN > 0 then we know the file is sensitve due to SSN
if [ $length -gt 0 ]; then
  isClean=false
  hasSSN=true
fi

#Checking to see if there are any strings named *SENSITIVE* in the file and if so we know that the file is sensitive due to it being marked that way
if `cat $1 | grep -Eoq "\*SENSITIVE\*"`; then
  isClean=false
  hasSensitive=true
fi

#Checking to see if the file is clean, has been marked sensitive due to *SENSITIVE* or if it has an SSN
if $isClean; then
  echo CLEAN
elif $hasSensitive; then
  echo SENSITIVE, MARKED SENSITIVE
elif $hasSSN; then
  echo SENSITIVE, SSN
fi
