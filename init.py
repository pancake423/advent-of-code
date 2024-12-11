# initialize a year's worth of advent of code puzzles:
# 1. create a directory with the current year
# 2. create a directory for each day 1-25
# 3. fill each with a copy of template.py
# 4. make a blank text file example.txt and input.txt
import os
import shutil

TEMPLATES = (
    ("template_main.py", "main.py"),
    ("template_sln.py", "solution.py")
)
TXT_FILES = ("example.txt", "input.txt")

year = input("year=")
try:
    os.mkdir(year)
except FileExistsError:
    print(f"Folder '{year}' already exists. Missing days and input files will be created, but existing scripts won't be overwritten.")

for i in range(25):
    path = os.path.join(year, "day_" + str(i+1))
    try:
        os.mkdir(path)
        for (template, name) in TEMPLATES:
            shutil.copy(template, path)
            os.rename(os.path.join(path, template), os.path.join(path, name))
    except FileExistsError:
        pass
    for filename in TXT_FILES:
        open(os.path.join(path, filename), "a").close()
