#!/bin/sh

OldFiles=false

#Getting list of all the files originally in the archive directory and comparing them to the new files if the archive directory exists
if [ -e archive ]; then
  OldFiles=$(ls archive | tr ' ' '\n')
fi

#Translating all the space characters to newlines
OldFiles=`echo $OldFiles | tr [:space:] '\n'`

#Isclean to determine whether to print out clean at the end or to see if i need to print out the reason why it isn't clean
IsClean=true

#Running the ae.sh script which extracts zip, gz, bz2, and tar files based on the first command line argument
sh ae.sh $1

echo SCANNING

#Some code that does not do what is needed
#for i in $(find archive -type f); do
#  test1=`sh sbs.sh ../badsites/badsite-100.csv $i`
#  test2=`sh sf.sh $i`
#
#  if echo $test1 | grep -q MALICIOUSURL; then
#    echo MALICIOUSURL
#    exit 1
#  elif echo $test2 | grep -q SENSITIVE; then
#    echo SENSITIVE
#    exit 1
#  fi
#done

#Now getting a list of the new files in the archive directory (These are the ones that are going to be scanned, and deleted at the end)
NewFiles=$(ls archive | tr ' ' '\n')

#Nested for loop which checks each file from NewFiles and OldFiles to see which ones do not match. It runs very slow if there are a lot of files
for i in $NewFiles; do
  IsNew=true

  #Looping through files in OldFiles
  for j in $OldFiles; do
    #If The Two files are equal to each other then it is not a new file so do nothing with it
    if [ $i = $j ]; then
      IsNew=false
    fi
  done

  #If this file is a new file, then we will loop through ever file and scan it for sensitive/malicious url using the sbs.sh and sf.sh scripts  and place it in two variables
  if $IsNew; then
    for j in `find archive/$i -type f`; do
      test1=`sh sbs.sh ../badsites/badsite-100.csv $j`
      test2=`sh sf.sh $j`

      #if there is a malicious url found or it is sensitive from the stdout of each shell script then echo out the reason and do not echo it again if it is found
      if echo $test1 | grep -q MALICIOUSURL; then
        if $IsClean; then
          echo MALICIOUSURL
          IsClean=false
        fi
      elif echo $test2 | grep -q SENSITIVE; then
        if $IsClean; then
          echo SENSITIVE
          IsClean=false
        fi
      fi
    done

    #Remove the file/directory after use
    rm -r "archive/$i"
  fi
done

#Echo CLEAN if nothing wrong is found
if $IsClean; then
  echo CLEAN
fi
