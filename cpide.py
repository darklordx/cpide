"""
The CPIDE is the entire frame.
Here is the layout of the CPIDE:
    On the LHS, there is the File Browser (filebrowswer.py)
    On the RHS, there is the Notebook (notebook.py)
        On the top of the Notebook, there are widgets (notebook.py)
        Below the widgets, there is the Code Editor (codeeditor.py)
            On the LHS of the Code Editor, there are line numbers (leftbar.py)
            Second to the left, there is the Complexity bar (leftbar.py)
            On the RHS of the Code Editor, there is the Code Editor Frame (codeeditor.py)
"""

import tkinter as tk
from tkinter import ttk
import platform
import os
import sys
from notebook import NotebookFrame
from filebrowser import FilebrowserFrame


class CPIDE(ttk.Frame):
    '''
        Main App
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.pack(expand=True, fill=tk.BOTH)
        self.initUI()
        self.initStyle()

    def initUI(self):
        self.parent.wm_iconbitmap("images/Icon.ico")

        # PanedWindow
        self.panedWindow = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panedWindow.pack(fill=tk.BOTH, expand=1)

        # InterpreterFrame
        self.filebrowserFrame = FilebrowserFrame(self.parent)
        # self.filebrowserFrame2 = FilebrowserFrame(self.parent)
        # self.filebrowserFrame.pack(side='left', fill='y')

        # NotebookFrame
        self.notebookFrame = NotebookFrame(self.parent)
        # self.notebookFrame.pack(side='right', expand=1, fill='both')
        self.notebookFrame.textPad.bind("<FocusIn>", self.textPadFocus)

        # add a variable for fileBrowserFrame to know the notebookFrame
        self.filebrowserFrame.notebookFrame = self.notebookFrame
        self.notebookFrame.filebrowserFrame = self.filebrowserFrame

        # add to PanedWindow
        self.panedWindow.add(self.filebrowserFrame)
        self.panedWindow.add(self.notebookFrame)
        # self.panedWindow.add(self.filebrowserFrame2)

    def textPadFocus(self, event=None):
        self.notebookFrame.updateMainWindow()

    def initStyle(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')



        # https://bugs.python.org/issue36468
        def fixed_map(option):
            # Fix for setting text colour for Tkinter 8.6.9
            # From: https://core.tcl.tk/tk/info/509cafafae
            #
            # Returns the style map for 'option' with any styles starting with
            # ('!disabled', '!selected', ...) filtered out.

            # style.map() returns an empty list for missing options, so this
            # should be future-safe.
            return [elm for elm in self.style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]

        self.style.configure("Treeview", background="yellow",
                             fieldbackground="black", foreground="black",
                             selectbackground='green')
        self.style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

        self.style.configure("Treeview.Heading", background="black", foreground='white', relief='flat')
        self.style.map('Treeview.Heading',
                       foreground=[('pressed', 'white'),
                                   ('focus', 'white'),
                                   ('active', 'white')],
                       background=[('pressed', '!focus', 'green'),
                                   ('active', 'green')],
                       highlightcolor=[('focus', 'green'),
                                       ('!focus', 'white')],
                       activerelief=[('pressed', 'groove'),
                                     ('!pressed', 'ridge')])

        self.style.configure('TCheckbutton', background='black',
                             fieldbackground='black', foreground='white')

        self.style.configure('TRadiobutton', background='black',
                             fieldbackground='black', foreground='white')
        self.style.map('TRadiobutton',
                       foreground=[('pressed', 'white'),
                                   ('focus', 'white'),
                                   ('active', 'white')],
                       background=[('pressed', '!focus', 'green'),
                                   ('active', 'green')],
                       highlightcolor=[('focus', 'green'),
                                       ('!focus', 'white')],
                       activerelief=[('pressed', 'groove'),
                                     ('!pressed', 'ridge')])

        self.style.configure('TSpinbox', background='black',
                             fieldbackground='black', foreground='white')

        self.style.configure('TNotebook', background='black',
                             fieldbackground='black', foreground='white')
        self.style.configure('TNotebook.Tab', background='black',
                             fieldbackground='black', foreground='white')
        self.style.map('TNotebook.Tab',
                       foreground=[('selected', 'yellow')],
                       background=[('selected', 'black')])

        self.style.configure('TFrame', background='black',
                             fieldbackground='black', foreground='white',
                             highlightcolor='white', highlightbackground='black',
                             highlightthickness=5)

        self.style.configure('TLabel', background='black',
                             fieldbackground='black', foreground='green')
        self.style.configure("White.TLabel", background='black',
                             fieldbackground='black', foreground="white")
        self.style.configure("Red.TLabel", background='black',
                             fieldbackground='black', foreground="red")

        self.style.configure('TPanedwindow', background='black',
                             fieldbackground='black', foreground='white')

        self.style.configure('TEntry', background='black',
                             fieldbackground='black', foreground='white')

        self.style.map('TEntry',
                       foreground=[('pressed', 'white'),
                                   ('focus', 'white'),
                                   ('active', 'white')],
                       background=[('pressed', '!focus', 'green'),
                                   ('active', 'green')],
                       highlightcolor=[('focus', 'green'),
                                       ('!focus', 'white')],
                       activerelief=[('pressed', 'groove'),
                                     ('!pressed', 'ridge')])

        self.style.configure('TButton', background='black',
                             fieldbackground='black', foreground='#FFFFFF')
        self.style.configure('Red', background='red')
        self.style.map('TButton',
                       foreground=[('pressed', 'white'),
                                   ('focus', 'white'),
                                   ('active', 'white')],
                       background=[('pressed', '!focus', 'green'),
                                   ('active', 'green')],
                       highlightcolor=[('focus', 'green'),
                                       ('!focus', 'white')],
                       activerelief=[('pressed', 'groove'),
                                     ('!pressed', 'ridge')])

        self.style.configure("TScrollbar", background="#1d1d1d",
                             foreground="#000000", activebackground="#000000",
                             troughcolor="#000000")
        self.style.map('TScrollbar',
                       foreground=[('pressed', '#424242'),
                                   ('focus', '#424242'),
                                   ('active', '#424242')],
                       background=[('pressed', '!focus', 'green'),
                                   ('active', 'green')],
                       highlightcolor=[('focus', 'green'),
                                       ('!focus', 'white')],
                       activerelief=[('pressed', 'groove'),
                                     ('!pressed', 'ridge')])


        self.style.configure('red.Horizontal.TProgressbar', background='red',
                             fieldbackground='red', foreground='red')

        self.style.configure('white.Horizontal.TProgressbar', background='blue',
                             fieldbackground='blue', foreground='blue')


def center(win):
    # Center the root screen
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


if __name__ == '__main__':
    root = tk.Tk()
    # root['bg'] = 'black'

    app = CPIDE(root)
    app.master.title('MoPad - Python IDE')
    app.master.minsize(width=800, height=600)

    center(root)
    app.mainloop()
