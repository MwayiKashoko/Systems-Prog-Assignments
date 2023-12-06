import requests
import sys
import re
import os
import urllib.request

urlName = None
url = None
website = ""
#regex used to find correct links
linkRegex = 'href="[^?/"]*"'
files = []
tarFiles = []

try:
    urlName = sys.argv[1]
    #url data
    url = requests.get(urlName)

    #making it so there are no new lines so I can read all the data at once unbroken
    for line in url:
        website += str(line)[2:-1].replace("\\n", "").strip()

except:
    print("Invalid URL")


#finds all the files and places them in an array
files = re.findall(linkRegex, website)

#Remove the annoying href="" at the start and end
for i in range(len(files)):
    files[i] = files[i][6:-1]

#if it is a tar file then we will put it in the analyze subdirectory
for f in files:
    if ".tar.gz" in f:
        #create the directory if it does not exist
        if not os.path.exists("analyze"):
            os.makedirs("analyze")

        if not os.path.exists("analyze/" + f):
            tarFiles.append("analyze/" + f)
            tarFile = requests.get(urlName + f)

            #copy over the contents
            with open("analyze/" + f, "wb") as file:
                file.write(tarFile.content)

#extracting the files and placing them in the extracted directory
for f in tarFiles:
    if not os.path.exists("extracted"):
        os.makedirs("extracted")

    #extraction
    os.system("tar -xvzf " + f + " -C extracted")

    
#listing every file in the extracted directory
files = os.listdir("extracted")

#Running the scanpcap program on every file in the extracted directory
for f in files:
    print("extracted/" + f)
    os.system("../scanpcap extracted/" + f)

#Removing all files in the extracted directory
for f in files:
    os.system("rm extracted/" + f)

files = os.listdir("analyze")

for f in files:
    os.system("rm analyze/" + f)
