import os
import sys

directoryName = ""
files = ""

try:
    directoryName = sys.argv[1]
    #Get the files
    files = os.listdir(directoryName)
except:
    print("ERROR")

#Print the file name as well as the stat command on that file
for f in files:
    print("\n" + f)

    os.system("stat " + "analyze/" + f)
    print()
