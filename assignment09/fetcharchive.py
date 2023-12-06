import requests
import sys
import re
import os
import urllib.request

urlName = None
url = None
website = ""
linkRegex = 'href="[^?/"]*"'
files = []

try:
    urlName = sys.argv[1]
    url = requests.get(urlName)

    for line in url:
        website += str(line)[2:-1].replace("\\n", "").strip()

except:
    print("Invalid URL")


files = re.findall(linkRegex, website)

for i in range(len(files)):
    files[i] = files[i][6:-1]

for f in files:
    if ".tar.gz" in f:
        if not os.path.exists("analyze"):
            os.makedirs("analyze")

        tarFile = requests.get(urlName + f)

        with open("analyze/" + f, "wb") as file:
            file.write(tarFile.content)
