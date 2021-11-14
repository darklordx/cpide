import re
import keyword
import platform
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import font
from configuration import Configuration
import importlib


class LeftBar(tk.Canvas):
    '''
        Abstract Canvas for LeftBar
    '''



    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        self.font_size = 14
        self.configFont()

    def configFont(self):
        '''font for linenumbers'''
        self.font = font.Font(family='monospace', size=self.font_size)
        # system = platform.system().lower()
        # if system == "windows":
        #     self.font = font.Font(family='monospace', size=self.font_size)
        # elif system == "linux":
        #     self.font = font.Font(family='monospace', size=self.font_size)
        # else:
        #     self.font = font.Font(family='monospace', size=self.font_size)

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        """redraw (to be overriden)"""
        self.delete("all")


class TextTimeComplexity(LeftBar):
    '''
        Canvas for Time Complexity Display
    '''

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            self.create_text(1, y, anchor="nw", font=self.font, text="asdf", fill='#FF00FF')
            i = self.textwidget.index("%s+1line" % i)


class TextLineNumbers(LeftBar):
    '''
        Canvas for Linenumbers
    '''

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(1, y, anchor="nw", font=self.font, text=linenum, fill='white')
            i = self.textwidget.index("%s+1line" % i)

