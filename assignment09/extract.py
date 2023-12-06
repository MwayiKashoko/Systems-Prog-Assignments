import os
import sys
import subprocess

fileName = ""

try:
    #Getting the file name
    fileName = sys.argv[1]

    #if the path does not exist create it
    if not os.path.exists("analyze"):
        os.makedirs("analyze")

    #extracting the file to the appropriate directory
    os.system("tar -xvzf " + fileName + " -C analyze")
except:
    print("Improper file name or file format")

