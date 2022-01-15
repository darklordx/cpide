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
        # self.font_size = 14
        self.configFont()

    def configFont(self):
        '''font for linenumbers'''
        if self.textwidget is None:
            self.font = font.Font(family='monospace', size=14)
        else:
            # Binds the font size to the textwidget's font size; it is stupid to use a second variable.
            self.font = font.Font(family='monospace', size=self.textwidget.font_size)

        # self.font = font.Font(family='monospace', size=self.font_size)
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

    def range_extract(self, s):
        if "range(" in s:
            # Todo: Slap a regex on this lmao
            start = s.index("range(") + len("range(")
            s = s[start:]
            if ")" in s:
                s = s[:s.index(")")].split(",")
                if all(i.isdigit() for i in s) and 1 <= len(s) <= 3:
                    start, end, jump = 0, 1, 1
                    # print("here")
                    if len(s) == 1:
                        end = int(s[0])
                    elif len(s) == 2:
                        start, end = map(int, s)
                    else:
                        start, end, jump = map(int, s)
                    return (end - start) // jump
        return None

    def flag_check(self, s):
        if "##" in s:
            s = s[s.rindex("##") + 2:].strip()
            if s.isdigit():
                return int(s)
        return None

    def calculate_complexity(self):
        lines = self.textwidget.get_complexity_tokens()
        lines = lines.split("\n")
        # print(lines[0])

        complexity = ["" for _ in range(len(lines))]
        recurrences = [1]

        i: int
        t: str
        for i, t in enumerate(lines):
            mult = None
            res: str = ""
            if "for" in t:
                res += "FOR "
                s = "".join(t.split())
                mult = self.range_extract(s)
            elif "while" in t:
                res += "WHILE "
            else:
                mult = 1  # There is no loop here...
                continue  # TODO: Implement many more things :D
            fmult = self.flag_check(t)
            if fmult:
                mult = fmult  # flag check overrides.
            if not mult:
                res += "(?) "
                mult = 1
            depth = (len(t) - len(t.lstrip(' '))) // 4
            recurrences = recurrences[:depth + 1]
            next = recurrences[-1] * mult
            recurrences.append(next)
            res += str(next)
            complexity[i + 1] = res
        return complexity

    def redraw(self, *args):
        """redraw line numbers"""
        self.delete("all")
        complexity = self.calculate_complexity()

        i = self.textwidget.index("@0,0")
        # i is just the line numbers,
        # but it only iterates over the line numbers
        # shown on the screen
        # print(tokens)
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            linenum = int(i.split(".")[0])
            # print(linenum)
            if complexity[linenum] != "":
                y = dline[1]
                self.create_text(10, y, anchor="nw", font=self.font, text=complexity[linenum], fill='#FF00FF')
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
            linenum = " " + str(i).split(".")[0]
            self.create_text(40, y, anchor="ne", font=self.font, text=linenum, fill='white')
            i = self.textwidget.index("%s+1line" % i)
