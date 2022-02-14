import re
import keyword
import platform
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import font

from typing import List

from configuration import Configuration
import importlib

from Polynomial import Polynomial

class LeftBar(tk.Canvas):
    """
        Abstract Canvas for LeftBar
    """

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
    """
        Canvas for Time Complexity Display
    """

    def configFont(self):
        '''font for linenumbers'''
        if self.textwidget is None:
            self.font = font.Font(family='monospace', size=10)
        else:
            # Binds the font size to the textwidget's font size; it is stupid to use a second variable.
            self.font = font.Font(family='monospace', size=2*self.textwidget.font_size//3)

    def range_extract(self, s):
        s.replace(" ", "")
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

    @staticmethod
    def flag_check(s):
        if "##" in s:
            s = s[s.rindex("##") + 2:].strip()
            if s.isdigit():
                return int(s)
            else:
                try:
                    return Polynomial.from_string(s)
                except:
                    return None
        return None

    def calculate_complexity(self):
        lines = self.textwidget.get_complexity_tokens()
        lines = lines.split("\n")
        # print(lines[0])

        complexity = ["" for _ in range(len(lines)+1)]  # Result strings.
        total_complexity: List[Polynomial] = []  # Cumulative Sum.
        recurrences: List[Polynomial] = [Polynomial(Z=1)]

        i: int
        t: str
        function_depth: int = -1
        function_name: str = None
        function_start: int = 0
        functions = {}
        total_complexity.append(Polynomial(Z = 0))
        for i, t in enumerate(lines):
            mult = None
            res: str = ""
            depth = (len(t) - len(t.lstrip(' '))) // 4
            recurrences = recurrences[:depth + 1]

            check_functions: str = ""
            k = t.replace(" ", "")
            for j in functions:
                if j + "(" in k:
                    check_functions = j

            if check_functions != "":
                res += f"JMP [{check_functions} -> {functions[check_functions]}] "
                mult = functions[check_functions]

            if "for " in t:
                res += "FOR "
                mult = self.range_extract(t)
            elif "while " in t:
                res += "WHILE "

            if depth <= function_depth:
                res += "END DEF "

                function_depth = -1
                functions[function_name] = total_complexity[i] - total_complexity[function_start]
                res += f"[{functions[function_name]} -> {function_name}] "
                mult = 1

            if "def " in t:
                function_name = self.function_name_extract(t)
                if function_name is not None:
                    function_depth = depth
                    res += "DEF " + function_name
                    mult = 1
                    function_start = i


            flag_mult = self.flag_check(t)
            if flag_mult:
                mult = flag_mult  # flag check overrides.
            if res != "" and (not mult):
                res += "(?) "
            if not mult:
                mult = 1

            next_complexity = recurrences[-1] * mult
            recurrences.append(next_complexity)
            if res != "":  # Otherwise, literally nothing happened :D
                res += str(next_complexity)

            # res += str(total_complexity[i])
            complexity[i + 1] = res

            total_complexity.append(total_complexity[i] + recurrences[-1])
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

    @staticmethod
    def function_name_extract(t):
        if ("(" not in t) or ("def " not in t):
            return None
        else:
            return t[t.index("def ") + len("def "):t.index("(")]


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
