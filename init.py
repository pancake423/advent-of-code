# initialize a year's worth of advent of code puzzles:
# 1. create a directory with the current year
# 2. create a directory for each day 1-25
# 3. fill each with a copy of template.py
# 4. make a blank text file example.txt and input.txt
import os
import shutil

TEMPLATE = "template.py"
SCRIPT_NAME = "main.py"
TXT_FILES = ["example.txt", "input.txt"]

year = input("year=")
try:
    os.mkdir(year)
except FileExistsError:
    print(f"Folder '{year}' already exists. Days that already have a folder will be ignored.")

for i in range(25):
    path = os.path.join(year, "day_" + str(i+1))
    try:
        os.mkdir(path)
        shutil.copy(TEMPLATE, path)
        os.rename(os.path.join(path, TEMPLATE), os.path.join(path, SCRIPT_NAME))
        for filename in TXT_FILES:
            open(os.path.join(path, filename), "w").close()
    except FileExistsError:
        print(f"ignored existing folder for day {i+1}.")
