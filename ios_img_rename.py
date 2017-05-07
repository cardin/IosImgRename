import tkinter
from tkinter import Tk, Frame, messagebox
import tkinter.filedialog as filedialog
import os
import re

class App(Frame):
	DIRECTORY = r'C:\Users\Cardin\OneDrive\YH and JH memories'
	WIDTH = 250
	HEIGHT = 150

	def __init__(self, parent):
		''' Constructor '''
		Frame.__init__(self, parent, background = 'white')
		self.parent = parent

		parent.withdraw() # hide the window for now
		self.main()

	def main(self):
		''' Main loop '''
		dirs = self.dir_selection()
		self.init_ui(dirs)
		
	def dir_selection(self):
		''' Get the directory to run '''
		desired_dirs = filedialog.askdirectory(initialdir = App.DIRECTORY, title = 'Please select a directory[s] to check for')
		
		if len(desired_dirs) == 0:
			messagebox.showinfo('Alert', 'No directory selected.\nApp will be terminating')
			exit(0)
		return desired_dirs

	def init_ui(self, dirs):
		screen_width = self.parent.winfo_screenwidth()
		screen_height = self.parent.winfo_screenheight()
		xpos = int((screen_width - App.WIDTH) / 2)
		ypos = int((screen_height - App.HEIGHT) / 2)
		geometry_str = "{0}x{1}+{2}+{3}".format(App.WIDTH, App.HEIGHT, xpos, ypos)
		self.parent.geometry(geometry_str)

		self.parent.title('IOS Image Rename')
		self.pack(fill=tkinter.BOTH, expand=1)

def main():
	root = Tk()
	app = App(root)
	root.mainloop()

def main2():
	if len(desired_dirs) == 0:
		print ("You didn't chose any directory")
		input("Press any key to close...")
		exit()
	else:
		print ("You chose %s" % desired_dirs)

	# Get a list of candidate filenames
	pattern = re.compile('^(\d+)(_\d+_iOS\.(?:jpg|jpeg|png))$')
	matchedFiles = []
	for file in os.listdir(desired_dirs):
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
		newFileUri = os.path.join(desired_dirs, newDatePrefix + patternResult.group(2))

		# rename
		oldFileUri = os.path.join(desired_dirs, file)
		os.rename(oldFileUri, newFileUri)

if __name__ == "__main__":
	main()
	print ("Done!")
	input("Press any key to close...")
	exit()
