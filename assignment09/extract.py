import os
import sys
import subprocess

fileName = ""

try:
    fileName = sys.argv[1]
    os.system("tar -xvzf " + fileName + " -C analyze")
except:
    print("Improper file name or file format")

