import tkinter
import tkinter.filedialog as filedialog
import os
import re

print ('')

# Get directory
## Prepare the GUI
root = tkinter.Tk()
root.withdraw() #hide the window

## Get the filename
currDir = os.getcwd()
desiredDir = filedialog.askdirectory(
	parent = root, initialdir = currDir, title = 'Please select a directory to check for')

if len(desiredDir) == 0:
	print ("You didn't chose any directory")
	input("Press any key to close...")
	exit()
else:
	print ("You chose %s" % desiredDir)

# Get a list of candidate filenames
pattern = re.compile('^(\d+)(_\d+_iOS\.(?:jpg|jpeg|png))$')
matchedFiles = []
for file in os.listdir(desiredDir):
	if pattern.search(file):
		matchedFiles.append(file)

if len(matchedFiles) == 0:
	print ("We found no files. Terminated.")
	input("Press any key to close...")
	exit()

# Ask for confirmation
print ("We found these files:")
for file in matchedFiles:
	print ("\t{0}".format(file))

print ("Click here to regain window focus.")
canGoAhead = input ("Is it okay? (Y/N)")
if canGoAhead.lower() == "n":
	print ("Terminated.")
	input("Press any key to close...")
	exit()

# Rename the files
for file in matchedFiles:
	
	# get the portions we need
	patternResult = pattern.match(file)
	datePrefix = patternResult.group(1)

	# create our new names
	newDatePrefix = "{0}-{1}-{2}".format(datePrefix[:4], datePrefix[4:6], datePrefix[6:])
	newFileUri = os.path.join(desiredDir, newDatePrefix + patternResult.group(2))

	# rename
	oldFileUri = os.path.join(desiredDir, file)
	os.rename(oldFileUri, newFileUri)

print ("Done!")
input("Press any key to close...")
exit()