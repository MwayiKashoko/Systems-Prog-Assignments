#!/bin/sh

#directory where archives to scan will be placed
if ! [ -e $1 ]; then
  echo "DIRECTORY DOES NOT EXIST"
  exit 1
fi

#Directory to place approved content
if ! [ -e $2 ]; then
  echo "DIRECTORY DOES NOT EXIST"
  exit 1
fi

#directory to place quarantined content
if ! [ -e $3 ]; then
  echo "DIRECTORY DOES NOT EXIST"
  exit 1
fi

#Place to log any decisions made by this script
if ! [ -e $4 ]; then
  mkdir $4
fi

logLine=`date,`

#File containing the malicious URLs
if ! [ -e $5 ]; then
  echo "THIS FILE DOES NOT EXIST"
  exit 1
fi

if ! [ -e extractedfiles ]; then
  mkdir extractedfiles
fi

#function that extracts file depending on type
extract_file() {
  #Allowing the function to access the argument sent in
  test -f “$1” -o -d “$1”

  reason1=none
  reason2=none

  #If the filetype matches one of the designated types, then my program will extract the file to the archive directory according tot he extension
  #If there is not a filetype that matches then the program exits because it is not possible to extract the given file
  CanExtract=true
  if [ $Filetype = zip ]; then
    echo Extracting zip file via unzip
    unzip -o $1 -d extractedfiles > /dev/null 2>&1
  elif [ $Filetype = bz2 ]; then
    echo Extracting bz2 file via tar
    bzcat $1 > extractedfiles/bz2extracted > /dev/null 2>&1
  elif [ $Filetype = gz ]; then
    echo Extracing gz file
    tar -xzvf $1 -C extractedfiles > /dev/null 2>&1
  elif [ $Filetype = tar ]; then
    echo Extracting tar file via tar
    tar -xf $1 -C extractedfiles > /dev/null 2>&1
  else
    reason1=CANNOTEXTRACT
    reason2="COULD NOT EXTRACT FILE"
    CanExtract=false
    cp $1 $3
  fi

  if $CanExtract; then
    for i in `find extractedfiles -type f`; do
      test1=`sh ../../tinker/sbs.sh ../../badsites/badsite-100.csv $i`
      test2=`sh $i`

      if "cat $test1 | grep MALICIOUSURL"; then
        reason1=MALICIOUSURL
        reason2="URLNAME IF I CAN FIGURE OUT HOW TO DO IT"
        mv $i $3
      elif "cat $test2 | grep SENSITIVE"; then
        reason1=SENSITIVE
        reason2="MARKED SENSITIVE"

        if "cat $test2 | grep SSN"; then;
          reason2="SSN"
        fi

        mv $i $3
      else
        logLine=`$logLine, date, $i, APPROVE`
        mv $i $2
      fi
    done
  fi

  if ! [ $reason1 = none ]; then
    logLine=`$logLine, date, $i, QUARANTINE, $reason1, $reason2`

    touch $3/$1.reason

    echo $3/$1 >> $3/$1.reason
    echo $reason1 >> $3/$1.reason
    echo $reason2 >> $3/$1.reason
  fi

  echo successfully extracted $Filetype file
}

NumFiles=`find $1 -type f | wc -l`

while true; do
  if [ $NumFiles -gt 0 ]; then
    for i in `find $1 -type f`; do
      #Filetype contains the extension of the file we are extracting in order to determine which command is needed
      Filetype=`echo i | rev | cut -d '.' -f1 | rev`

      #If the command argument exists in the directory then the code will continue to run
      extract_file $i

      NumFiles=$(($NumFiles-1))
    done
  else
    sleep 1
  fi
done

appendexit() {
  logLine=`$logLine, date`
  echo $logLine >> $4
}

trap appendexit SIGINT
