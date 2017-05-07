from tkinter import Tk, Frame, Label, Scrollbar, Listbox, Button, messagebox, \
	BOTH, EXTENDED, RIGHT, LEFT, END
import tkinter.filedialog as filedialog
import os
import re

class App(Frame):
	DIRECTORY = r'C:\Users\Cardin\OneDrive\YH and JH memories'
	WIDTH = 400
	HEIGHT = 310

	FILE_PATTERN = re.compile('^(\d+)(_\d+_iOS\.(?:jpg|jpeg|png))$')

	def __init__(self, parent):
		''' Constructor '''
		Frame.__init__(self, parent)
		self.parent = parent

		parent.withdraw() # hide the window for now

		# main loop
		self.dir_selection()
		self.init_ui()
		
	def dir_selection(self):
		''' Get the directory to run '''
		self.desired_dir = desired_dir = filedialog.askdirectory(initialdir = App.DIRECTORY, title = 'Please select a directory to check for')
		
		if len(desired_dir) == 0:
			messagebox.showinfo('Alert', 'No directory selected.\nApp will be terminating')
			exit(0)

	def init_ui(self):
		''' Get the UI up '''
		dir = self.desired_dir

		self.parent.title('IOS Image Rename')
		self.pack() # as tight as possible

		# Label
		label = Label(self, text='Files to exclude:')
		label.pack()

		# List Frame - label + listbox + scrollbar
		list_frame = Frame(self)
		list_frame.pack(pady=5) # as tight as possible
		scrollbar = Scrollbar(list_frame, orient='vertical')
		self.listnodes = listnodes = Listbox(list_frame, selectmode=EXTENDED, yscrollcommand=scrollbar.set,\
			width=40, height=15) # width = #char, height = #lines
		scrollbar.config(command=listnodes.yview)

		scrollbar.pack(side=RIGHT, fill='y') # as long as needed
		listnodes.pack(side=LEFT, fill='y') # as long as stated in constructor

		## Iterate though the directory
		for file in os.listdir(dir):
			if App.FILE_PATTERN.search(file):
				listnodes.insert(END, file)
		if listnodes.size() == 0:
			messagebox.showwarning('No files', 'No matching files found in {0}.\nApp will be terminating'.format(dir))
			exit(0)

		# Button Frame - Ok button
		btn_frame = Frame(self)
		btn_frame.pack(fill='x') # as wide as parent frame allows
		self.ok_btn = ok_btn = Button(btn_frame, text="Ok", width=15, command=self.rename)
		ok_btn.pack(side=RIGHT, fill='y')

		# Display window
		self.center_ui(App.WIDTH, App.HEIGHT)
		self.parent.deiconify() # Show window again

	def center_ui(self, width, height):
		''' Centers the UI based on given dimensions '''
		screen_width = self.parent.winfo_screenwidth()
		screen_height = self.parent.winfo_screenheight()
		xpos = int((screen_width - width) / 2)
		ypos = int((screen_height - height) / 2)
		geometry_str = "{0}x{1}+{2}+{3}".format(width, height, xpos, ypos)
		self.parent.geometry(geometry_str)

	def rename(self):
		''' Begin renaming the given list of files '''
		dir = self.desired_dir
		listnodes = self.listnodes

		# disable button
		self.ok_btn.config(state='disabled')

		# Get list of selected files
		selected = set([listnodes.get(idx) for idx in listnodes.curselection()])
		unselected = set([listnodes.get(idx) for idx in range(listnodes.size())])
		target_files = unselected - selected

		for file in target_files:
	
			# get the portions we need
			pattern_result = self.FILE_PATTERN.match(file)
			date_prefix = pattern_result.group(1)

			# create our new names
			newdate_prefix = "{0}-{1}-{2}".format(date_prefix[:4], date_prefix[4:6], date_prefix[6:])
			new_name = os.path.join(dir, newdate_prefix + pattern_result.group(2))

			# rename
			old_name = os.path.join(dir, file)
			os.rename(old_name, new_name)

		messagebox.showinfo('Done', 'Processing is completed!\n{0} file[s] renamed.'.format(len(target_files)))
		self.parent.quit()

def main():
	''' Main function '''
	root = Tk()
	app = App(root)
	root.mainloop()

if __name__ == "__main__":
	main()
	exit(0)
