''' Renames images that are from IOS camera '''
import pickle
import os
from os import path
import re
from tkinter import Tk, Frame, Label, Scrollbar, Listbox, Button, messagebox, \
    EXTENDED, RIGHT, LEFT, END
import tkinter.filedialog as filedialog


class App(Frame):
    ''' The application model '''
    CONFIG_PATH = 'config.bin'
    WIDTH = 400
    HEIGHT = 310

    FILE_PATTERN = re.compile(
        r'^(\d+)(_\d+_iOS\.(?:jpg|jpeg|png|mov|mp4))$', re.IGNORECASE)

    def __init__(self, parent: Tk) -> None:
        ''' Constructor '''
        Frame.__init__(self, parent)
        self.parent = parent

        parent.withdraw()  # hide the window for now

        # main loop
        self.dir_selection()
        self.init_ui()

    def dir_selection(self) -> None:
        ''' Get the directory to run '''
        self.desired_dir = None

        # load previous directory
        if path.exists(App.CONFIG_PATH):
            with open(App.CONFIG_PATH, 'rb') as fstream:
                self.desired_dir = pickle.load(fstream)

        # prompt for directory
        self.desired_dir = \
            filedialog.askdirectory(
                initialdir=self.desired_dir, title='Please select a directory to check for')

        if not self.desired_dir:  # empty string
            messagebox.showinfo(
                'Alert', 'No directory selected.\nApp will be terminating')
            exit(0)

        # save previous directory
        with open(App.CONFIG_PATH, 'wb') as fstream:
            pickle.dump(self.desired_dir, fstream)

    def init_ui(self) -> None:
        ''' Get the UI up '''
        self.parent.title('IOS Image Rename')
        self.pack()  # as tight as possible

        # Label
        label = Label(self, text='Files to exclude:')
        label.pack()

        # List Frame - listbox + scrollbar
        list_frame = Frame(self)
        list_frame.pack(pady=5)  # as tight as possible
        scrollbar = Scrollbar(list_frame, orient='vertical')
        self.listnodes = listnodes = \
            Listbox(list_frame, selectmode=EXTENDED,
                    yscrollcommand=scrollbar.set, width=40, height=15)
        # width = #char, height = #lines
        scrollbar.config(command=listnodes.yview)

        scrollbar.pack(side=RIGHT, fill='y')  # as long as needed
        listnodes.pack(side=LEFT, fill='y')  # as long as stated in constructor

        # Iterate though the directory
        for dirpath, _, filenames in os.walk(self.desired_dir):
            for filename in filenames:
                if App.FILE_PATTERN.search(filename):
                    full_path = path.join(dirpath, filename)
                    listnodes.insert(END, path.relpath(
                        full_path, self.desired_dir))
        if listnodes.size() == 0:
            messagebox.showwarning('No files',
                                   'No matching files found in {0}.' +
                                   '\nApp will be terminating'.format(self.desired_dir))
            exit(0)

        # Button Frame - Ok button
        btn_frame = Frame(self)
        btn_frame.pack(fill='x')  # as wide as parent frame allows
        self.ok_btn = ok_btn = Button(
            btn_frame, text="Ok", width=15, command=self.rename)
        ok_btn.pack(side=RIGHT, fill='y')

        # Display window
        self.center_ui(App.WIDTH, App.HEIGHT)
        self.parent.deiconify()  # Show window again

    def center_ui(self, width: int, height: int) -> None:
        ''' Centers the UI based on given dimensions '''
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        xpos = int((screen_width - width) / 2)
        ypos = int((screen_height - height) / 2)
        geometry_str = "{0}x{1}+{2}+{3}".format(width, height, xpos, ypos)
        self.parent.geometry(geometry_str)

    def rename(self) -> None:
        ''' Begin renaming the given list of files '''
        target_dir = self.desired_dir
        listnodes = self.listnodes

        # disable button
        self.ok_btn.config(state='disabled')

        # Get list of selected files
        selected = set([listnodes.get(idx)
                        for idx in listnodes.curselection()])
        unselected = set([listnodes.get(idx)
                          for idx in range(listnodes.size())])
        target_files = unselected - selected

        for file_ in target_files:
            dirname, filename = path.split(file_)

            # get the portions we need
            pattern_result = App.FILE_PATTERN.match(filename)
            date_prefix = pattern_result.group(1)

            # create our new names
            newdate_prefix = "{0}-{1}-{2}".format(
                date_prefix[:4], date_prefix[4:6], date_prefix[6:])
            new_name = os.path.join(target_dir,
                                    dirname, newdate_prefix + pattern_result.group(2))

            # rename
            old_name = os.path.join(target_dir, file_)
            os.rename(old_name, new_name)

        messagebox.showinfo('Done',
                            'Processing is completed!\n' +
                            '{0} file[s] renamed.'.format(len(target_files)))
        self.parent.quit()


def main() -> None:
    ''' Main function '''
    root = Tk()
    _ = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    exit(0)
