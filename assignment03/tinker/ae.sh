#!/bin/sh

#If the archive directory is not present then make that directory
if ! [ -e archive ]; then
  echo Creating archive directory because it is not present
  mkdir archive
fi

#Filetype contains the extension of the file we are extracting in order to determine which command is needed
Filetype=`echo $1 | rev | cut -d '.' -f1 | rev`

#function that extracts file depending on type
extract_file() {
  #Allowing the function to access the argument sent in
  test -f “$1” -o -d “$1”

  #If the filetype matches one of the designated types, then my program will extract the file to the archive directory according tot he extension
  #If there is not a filetype that matches then the program exits because it is not possible to extract the given file
  if [ $Filetype = zip ]; then
    echo Extracting zip file via unzip
    unzip -o $1 -d archive > /dev/null 2>&1
  elif [ $Filetype = bz2 ]; then
    echo Extracting bz2 file via tar
    bzcat $1 > archive/bz2extracted > /dev/null 2>&1
  elif [ $Filetype = gz ]; then
    echo Extracing gz file
    tar -xzvf $1 -C archive > /dev/null 2>&1
  elif [ $Filetype = tar ]; then
    echo Extracting tar file via tar
    tar -xf $1 -C archive > /dev/null 2>&1
  else 
    echo file is not one of the valid types: zip, bz2, gz, tar
    exit 1
  fi

  echo successfully extracted $Filetype file
}

#If the command argument exists in the directory then the code will continue to run
if [ -e $1 ]; then
  echo the file exists
  extract_file $1
else
  echo the file does not exist
  exit 1
fi
