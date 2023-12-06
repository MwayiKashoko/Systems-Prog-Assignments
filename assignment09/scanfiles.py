import os
import sys

directoryName = ""
files = ""

try:
    directoryName = sys.argv[1]
    files = os.listdir(directoryName)
except:
    print("ERROR")

for f in files:
    print("\n" + f)

    os.system("stat " + "analyze/" + f)
    print()
