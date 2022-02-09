"""
The Notebook is the entire RHS of the screen.
It contains multiple Code Editors.
The below code does these things:
 - All of the buttons in the top row.
 - Switching between Code Editors.
 - The Tooltips give little pop-ups when looking at widgets.
"""

import random
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from codeeditor import CodeeditorFrame, IOFrame
from dialog import OpenFileDialog, SettingsDialog, MessageDialog, SaveFileDialog
from configuration import Configuration
import keyword
import os
import gc
import webbrowser
import subprocess


class NotebookFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        try:
            self.overlord = self.parent.parent
        except:
            self.overlord = None

        self.filebrowserFrame = None

        self.runContinuousFlag = False

        self.continuousCount = 0
        self.initUI()

    def initUI(self):
        self.style = ttk.Style()

        self.buttonFrame = ttk.Frame(self)
        self.initButtons()
        self.notebook = ttk.Notebook(self)

        self.buttonFrame.pack(side=tk.TOP, fill=tk.X)
        self.notebook.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.newCP()
        self.new()

    def initButtons(self):
        HOMEPATH = os.path.dirname(__file__) + '/'

        # Buttons
        newIcon = tk.PhotoImage(file=HOMEPATH + 'images/new.png')
        newButton = ttk.Button(self.buttonFrame, image=newIcon, command=self.new)
        newButton.image = newIcon
        newButton.pack(side=tk.LEFT)
        newButton_ttp = CreateToolTip(newButton, 'New')

        openIcon = tk.PhotoImage(file=HOMEPATH + 'images/open.png')
        openButton = ttk.Button(self.buttonFrame, image=openIcon, command=self.openFileDialog)
        openButton.image = openIcon
        openButton.pack(side=tk.LEFT)
        openButton_ttp = CreateToolTip(openButton, 'Open')

        saveIcon = tk.PhotoImage(file=HOMEPATH + 'images/save.png')
        saveButton = ttk.Button(self.buttonFrame, image=saveIcon, command=self.save)
        saveButton.image = saveIcon
        saveButton.pack(side=tk.LEFT)
        saveButton_ttp = CreateToolTip(saveButton, 'Save')

        saveAsIcon = tk.PhotoImage(file=HOMEPATH + 'images/saveAs.png')
        saveAsButton = ttk.Button(self.buttonFrame, image=saveAsIcon, command=self.saveAs)
        saveAsButton.image = saveAsIcon
        saveAsButton.pack(side=tk.LEFT)
        saveAsButton_ttp = CreateToolTip(saveAsButton, 'Save As')

        printIcon = tk.PhotoImage(file=HOMEPATH + 'images/print.png')
        printButton = ttk.Button(self.buttonFrame, image=printIcon, command=self.printer)
        printButton.image = printIcon
        printButton.pack(side=tk.LEFT)
        printButton_ttp = CreateToolTip(printButton, "Print to HTML-File")
        #
        # undoIcon = tk.PhotoImage(file=HOMEPATH + 'images/undo.png')
        # undoButton = ttk.Button(self.buttonFrame, image=undoIcon, command=self.undo)
        # undoButton.image = undoIcon
        # undoButton.pack(side=tk.LEFT)
        # undoButton_ttp = CreateToolTip(undoButton, 'Undo')
        #
        # redoIcon = tk.PhotoImage(file=HOMEPATH + 'images/redo.png')
        # redoButton = ttk.Button(self.buttonFrame, image=redoIcon, command=self.redo)
        # redoButton.image = redoIcon
        # redoButton.pack(side=tk.LEFT)
        # redoButton_ttp = CreateToolTip(redoButton, "Redo")

        zoomInIcon = tk.PhotoImage(file=HOMEPATH + 'images/zoomIn.png')
        zoomInButton = ttk.Button(self.buttonFrame, image=zoomInIcon, command=self.zoomIn)
        zoomInButton.image = zoomInIcon
        zoomInButton.pack(side=tk.LEFT)
        zoomInButton_ttp = CreateToolTip(zoomInButton, "Zoom In")

        zoomOutIcon = tk.PhotoImage(file=HOMEPATH + 'images/zoomOut.png')
        zoomOutButton = ttk.Button(self.buttonFrame, image=zoomOutIcon, command=self.zoomOut)
        zoomOutButton.image = zoomOutIcon
        zoomOutButton.pack(side=tk.LEFT)
        zoomOutButton_ttp = CreateToolTip(zoomOutButton, "Zoom Out")

        settingsIcon = tk.PhotoImage(file=HOMEPATH + 'images/settings.png')
        settingsButton = ttk.Button(self.buttonFrame, image=settingsIcon, command=self.settings)
        settingsButton.image = settingsIcon
        settingsButton.pack(side=tk.LEFT)
        settingsButton_ttp = CreateToolTip(settingsButton, "Show Settings")

        self.scoreBar = ttk.Progressbar(self.buttonFrame, orient = tk.HORIZONTAL, length = 100, mode = 'determinate')
        self.scoreBar.pack(side=tk.RIGHT)
        scoreBar_ttp = CreateToolTip(self.scoreBar, "This scorebar will show you how many lines of output are correct")
        self.scoreBar['value'] = 100


        runContinuous = tk.PhotoImage(file=HOMEPATH + 'images/run.png')
        runContinuousButton = ttk.Button(self.buttonFrame, image=runContinuous, command=self.runContinuous)
        runContinuousButton.image = runContinuous
        runContinuousButton.pack(side=tk.RIGHT)
        runContinuousButton_ttp = CreateToolTip(runContinuousButton, "Run Continuously")

        runAgainstIcon = tk.PhotoImage(file=HOMEPATH + 'images/run.png')
        runAgainstButton = ttk.Button(self.buttonFrame, image=runAgainstIcon, command=self.runAgainst)
        runAgainstButton.image = runAgainstIcon
        runAgainstButton.pack(side=tk.RIGHT)
        runAgainstButton_ttp = CreateToolTip(runAgainstButton, "Run Against Input File")

        runIcon = tk.PhotoImage(file=HOMEPATH + 'images/run.png')
        runButton = ttk.Button(self.buttonFrame, image=runIcon, command=self.run)
        runButton.image = runIcon
        runButton.pack(side=tk.RIGHT)
        runButton_ttp = CreateToolTip(runButton, "Run File")

        terminalIcon = tk.PhotoImage(file=HOMEPATH + 'images/terminal.png')
        terminalButton = ttk.Button(self.buttonFrame, image=terminalIcon, command=self.terminal)
        terminalButton.image = terminalIcon
        terminalButton.pack(side=tk.RIGHT)
        terminalButton_ttp = CreateToolTip(terminalButton, 'Open Terminal')

        interpreterIcon = tk.PhotoImage(file=HOMEPATH + 'images/interpreter.png')
        interpreterButton = ttk.Button(self.buttonFrame, image=interpreterIcon, command=self.interpreter)
        interpreterButton.image = interpreterIcon
        interpreterButton.pack(side=tk.RIGHT)
        interpreterButton_ttp = CreateToolTip(interpreterButton, "Open Python Interpreter")

        '''
        viewIcon = tk.PhotoImage(file=self.dir + 'images/view.png')
        viewButton = ttk.Button(self.rightBottomFrame, image=viewIcon, command=self.overview)
        viewButton.image = viewIcon
        viewButton.pack(side=tk.RIGHT)
        self.createToolTip(viewButton, 'Class Overview')
        '''

        searchIcon = tk.PhotoImage(file=HOMEPATH + 'images/search.png')
        searchButton = ttk.Button(self.buttonFrame, image=searchIcon, command=self.search)
        searchButton.image = searchIcon
        searchButton.pack(side=tk.RIGHT)
        searchButton_ttp = CreateToolTip(searchButton, "Search")

        self.searchBox = tk.Entry(self.buttonFrame, bg='black', fg='white')
        self.searchBox.configure(cursor="xterm green")
        self.searchBox.configure(insertbackground="red")
        self.searchBox.configure(highlightcolor='#448dc4')

        # self.searchBox.bind('<Key>', self.OnSearchBoxChange)
        self.searchBox.bind('<Return>', self.search)
        self.searchBox.pack(side=tk.RIGHT, padx=5)

        # self.autoRun = tk.Button(root, image = )

    def openIOFile(self, filename, event=None):
        self.codeeditorFrame = IOFrame(self)

        self.notebook.add(self.codeeditorFrame, text=filename)

        self.textPad = self.codeeditorFrame.textPad

        self.notebook.bind("<ButtonRelease-1>", self.tabChanged)
        self.notebook.bind("<ButtonRelease-3>", self.closeContext)

        x = len(self.notebook.tabs()) - 1
        self.notebook.select(x)
        self.tabChanged()

        try:
            # open file for reading
            with open(filename, 'r') as f:
                text = f.read()

            # update textPad
            self.textPad.delete('1.0', tk.END)
            self.textPad.insert("1.0", text)
            self.textPad.filename = filename
            self.textPad.tag_all_lines()

        except Exception as e:
            MessageDialog(self, 'Error', '\n' + str(e) + '\n')
            return

    def newCP(self):
        try:
            open("in.txt")
        except FileNotFoundError:
            with open("in.txt", "w") as f:
                f.write("This is your input file. Write the desired input here.")

        self.openIOFile("in.txt")

        try:
            open("res.txt")
        except FileNotFoundError:
            with open("res.txt", "w") as f:
                f.write("This is your result file. Write the desired output here. "
                        "The real output will be written to out.txt")
        self.openIOFile("res.txt")

    def new(self, event=None):
        self.codeeditorFrame = CodeeditorFrame(self)
        self.notebook.add(self.codeeditorFrame, text='noname')
        # self.frameName = self.notebook.select()

        self.textPad = self.codeeditorFrame.textPad

        self.notebook.bind("<ButtonRelease-1>", self.tabChanged)
        self.notebook.bind("<ButtonRelease-3>", self.closeContext)

        x = len(self.notebook.tabs()) - 1
        self.notebook.select(x)
        self.tabChanged()

    def open(self, filename=None, event=None):
        if not filename:
            filename = filedialog.askopenfilename()

            if not filename:
                return

        try:
            # open file for reading
            with open(filename, 'r') as f:
                text = f.read()

            # update textPad
            self.textPad.delete('1.0', tk.END)
            self.textPad.insert("1.0", text)
            self.textPad.filename = filename
            self.textPad.tag_all_lines()

        except Exception as e:
            MessageDialog(self, 'Error', '\n' + str(e) + '\n')
            return

        # update tab text
        file = self.textPad.filename.split('/')[-1]
        id = self.notebook.index(self.notebook.select())
        self.notebook.tab(id, text=file)

        # generate tabChanged event (get new textPad, etc)
        self.tabChanged()

        # update autocompleteList from codeeditor
        # self.textPad.updateAutoCompleteList()
        self.filebrowserFrame.refreshTree()

    def openFile(self, filename, event=None):
        self.codeeditorFrame = CodeeditorFrame(self)

        self.notebook.add(self.codeeditorFrame, text=filename)
        # self.frameName = self.notebook.select()

        self.textPad = self.codeeditorFrame.textPad

        self.notebook.bind("<ButtonRelease-1>", self.tabChanged)
        self.notebook.bind("<ButtonRelease-3>", self.closeContext)

        x = len(self.notebook.tabs()) - 1
        self.notebook.select(x)
        self.tabChanged()

        try:
            # open file for reading
            with open(filename, 'r') as f:
                text = f.read()

            # update textPad
            self.textPad.delete('1.0', tk.END)
            self.textPad.insert("1.0", text)
            self.textPad.filename = filename
            self.textPad.tag_all_lines()

        except Exception as e:
            MessageDialog(self, 'Error', '\n' + str(e) + '\n')
            return

    def openFileDialog(self):
        dialog = OpenFileDialog(parent=self.parent, notebookFrame=self, title='Open')

    def save(self, event=None):
        if not self.textPad:
            return
        if not self.textPad.filename:
            self.saveAs()
        filename = self.textPad.filename
        if not filename:
            return
        self._saveUpdate(filename)

    def saveAs(self, event=None):
        dialog = SaveFileDialog(self, "Save as")
        filename = dialog.filename
        if not filename:
            return
        self._saveUpdate(filename)

    def _saveUpdate(self, filename):
        try:
            with open(filename, 'w') as f:
                text = self.textPad.get("1.0", 'end-1c')
                f.write(text)

        except Exception as e:
            MessageDialog(self, 'Error', '\n' + str(e) + '\n')
        # update textPad
        self.textPad.filename = filename

        # update tab text
        file = self.textPad.filename.split('/')[-1]
        id = self.notebook.index(self.notebook.select())
        self.notebook.tab(id, text=file)

        # generate tabChanged event (get new textPad, etc)
        self.tabChanged()
        self.filebrowserFrame.refreshTree()

    def quicksave(self, event=None):
        if not self.textPad.filename:
            # QUICK RUN
            random_hex = '%08X' % random.randint(0, 256 ** 4 - 1)
            self.textPad.filename = f"tmp{random_hex}.py"
        self.save()
        return self.textPad.filename

    def printer(self, event=None):
        # print file to html
        if not self.textPad:
            return

        if not self.textPad.filename:
            return

        text = self.textPad.get("1.0", 'end-1c')
        filename = self.textPad.filename.split('/')[-1]
        kwList = keyword.kwlist

        output = "<head>" + filename + "</head>\n"
        output += "<body>\n"
        output += '<pre><code>\n'
        output += text + '\n'
        output += '</pre></code>\n'
        output += "</body>"

        fname = self.textPad.filename + "_.html"

        with open(fname, "w") as f:
            f.write(output)

        try:
            webbrowser.open(fname)

        except Exception as e:
            MessageDialog(self, 'Error', '\n' + str(e) + '\n')
            return

        self.filebrowserFrame.refreshTree()

    def undo(self, event=None):
        if self.textPad:
            self.textPad.undo()

    def redo(self, event=None):
        if self.textPad:
            self.textPad.redo()

    def configFont(self):
        """
        Propagates font size to textpad and leftbars.
        """
        self.textPad.configFont()
        self.textPad.linenumber.configFont()
        self.textPad.linenumber.redraw()
        self.textPad.complexity.configFont()
        self.textPad.complexity.redraw()

    def zoomIn(self, event=None):
        if not self.textPad:
            return
        if self.textPad.font_size < 30:
            self.textPad.font_size += 1
            self.configFont()

    def zoomOut(self, event=None):
        if not self.textPad:
            return
        if self.textPad.font_size > 5:
            self.textPad.font_size -= 1
            self.configFont()

    def settings(self, event=None):
        dialog = SettingsDialog(self)

    def run(self, event=None, openshell = True):
        if not self.textPad:
            return
        self.quicksave()
        filepath = self.textPad.filename

        file = filepath.split('/')[-1]

        c = Configuration()  # -> in configuration.py
        system = c.getSystem()
        if openshell:
            runCommand = c.getRun(system).format(file)
        else:
            runCommand = c.getRunNoShell(system).format(file)

        subprocess.call(runCommand, shell=True)

    def add_prefix(self):
        """
        Add prefix to beginning of script to redirect IO.
        """

        PREFIX = r"""
# Here is some code that redirects io.
_input_stream = open("in.txt")
_output_stream = open("out.txt", "w", buffering=1)

def input():
    s = _input_stream.readline()
    if s[-1]=="\n":
        return s[:-1]
    else:
        return s

def print(*s):
    _output_stream.write(" ".join(map(str,s))+"\n")
# User Code Below
"""
        code = self.textPad.get("1.0", tk.END)
        code = PREFIX + code
        #print(code)
        return code

    def runContinuous(self):
        if self.runContinuousFlag:
            self.runContinuousFlag = False
        else:
            self.runContinuousFlag = True
            # self.continuousCount = 30

            self.runContinuousLoop()

    def runContinuousLoop(self):
        if not self.runContinuousFlag:
            return
        # if self.continuousCount < 0:
        #     self.runContinuousFlag=False
        #     return

        self.runAgainst()

        # self.continuousCount -= 1
        self.after(ms=5000, func=self.runContinuousLoop)

    """
    This compares the results.txt file against the output file.
    """
    def getscore(self) -> float:
        score = 0
        try:
            with open("out.txt") as out:
                o = out.readlines()
            with open("res.txt") as res:
                r = res.readlines()
        except FileNotFoundError:
            return -1

        if len(o) == len(r) > 0:
            for i, j in zip(o, r):
                if i == j:
                    score += 1
            score /= len(r)
        else:
            return -1
        return score

    def updatescore(self):
        score = self.getscore()
        if score == -1:
            self.scoreBar['style'] = "red.Horizontal.TProgressbar"
            self.scoreBar['value'] = 100

        else:

            self.scoreBar['style'] = "white.Horizontal.TProgressbar"
            self.scoreBar['value'] = score*100

    def runAgainst(self):

        if not self.textPad:
            return
        self.quicksave()
        code = self.add_prefix()

        filepath = self.textPad.filename
        print(filepath)

        random_hex = 'RA%08X' % random.randint(0, 256 ** 4 - 1)

        dot = filepath.rindex(".")

        try:
            what = filepath.rindex("/")
        except ValueError:
            what = -1
        tmp_filepath = filepath[:what+1] + 'tmp' + filepath[what+1:dot] + random_hex + filepath[dot:]

        with open(tmp_filepath, "w") as f:
            f.write(code)

        c = Configuration()  # -> in configuration.py
        system = c.getSystem()

        file = tmp_filepath.split('/')[-1]
        runCommand = c.getRunNoShell(system).format(file)

        try:
            open("in.txt")
        except FileNotFoundError:
            with open("in.txt", "w") as f:
                f.write("This is your input file. Write the desired input here.")
            MessageDialog(self, "Error", "No in.txt file provided. I have created one for you.")
            self.openFile("in.txt")

        try:
            open("res.txt")
        except FileNotFoundError:
            with open("res.txt", "w") as f:
                f.write("This is your result file. Write the desired output here. "
                        "The real output will be written to out.txt")
            MessageDialog(self, "Error", "No res.txt file provided. I have created one for you.")
            self.openFile("res.txt")

        try:
            open("out.txt")
        except FileNotFoundError:
            self.openFile("out.txt")

        self.updatescore()

        subprocess.call(runCommand, shell=True)


    def terminal(self, event=None):
        c = Configuration()  # -> in configuration.py
        system = c.getSystem()
        terminalCommand = c.getTerminal(system)

        try:
            subprocess.call(terminalCommand, shell=True)
        except Exception as e:
            dialog = MessageDialog(self, 'Error', '\n' + str(e) + '\n')
            return

    def interpreter(self, event=None):
        c = Configuration()  # -> in configuration.py
        system = c.getSystem()
        interpreterCommand = c.getInterpreter(system)

        subprocess.call(interpreterCommand, shell=True)

    def search(self, start=None):
        if not self.textPad:
            return

        self.textPad.tag_remove('sel', "1.0", tk.END)

        toFind = self.searchBox.get()
        pos = self.textPad.index(tk.INSERT)
        result = self.textPad.search(toFind, str(pos), stopindex=tk.END)

        if result:
            length = len(toFind)
            row, col = result.split('.')
            end = int(col) + length
            end = row + '.' + str(end)
            self.textPad.tag_add('sel', result, end)
            self.textPad.mark_set('insert', end)
            self.textPad.see(tk.INSERT)
            self.textPad.focus_force()
        else:
            self.textPad.mark_set('insert', '1.0')
            self.textPad.see(tk.INSERT)
            self.textPad.focus()
            # self.setEndMessage(400)
            self.searchBox.focus()
            return

    # def setEndMessage(self, seconds):
    #         # pathList = __file__.replace('\\', '/')
    #         pathList = __file__.split('/')[:-1]
    #
    #         self.dir = ''
    #         for item in pathList:
    #             self.dir += item + '/'
    #
    #         canvas = tk.Canvas(self.textPad, width=64, height=64)
    #         # x = self.textPad.winfo_width() / 2
    #         # y = self.textPad.winfo_height() / 2
    #
    #         canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    #         image = tk.PhotoImage(file = self.dir + 'images/last.png')
    #         canvas.create_image(0, 0,  anchor=tk.NW, image=image)
    #
    #         self.textPad.update()
    #         self.after(seconds, self.textPad.entry.config(text='---'))
    #
    #         canvas.destroy()
    #         self.textPad.update()

    def tabChanged(self, event=None):
        tabs = self.notebook.tabs()
        try:
            id = self.notebook.index(self.notebook.select())
        except:
            return

        name = tabs[id]
        codeframe = self.notebook._nametowidget(name)

        self.textPad = codeframe.textPad

        self.updateMainWindow()
        self.textPad.focus()

    def updateMainWindow(self, event=None):
        if not self.textPad:
            return

        if not self.overlord:
            if self.textPad.filename:
                self.parent.title(self.textPad.filename)
            else:
                self.parent.title("CPIDE - Competitive Programming IDE")
        else:
            if self.textPad.filename:
                self.overlord.title(self.textPad.filename)
            else:
                self.overlord.title("CPIDE - Competitive Programming IDE")

    def closeContext(self, event=None):
        tabs = self.notebook.tabs()
        if not tabs:
            return

        menu = tk.Menu(self.notebook, tearoff=False, background='#000000', foreground='white',
                       activebackground='blue', activeforeground='white')
        menu.add_command(label='Close', compound=tk.LEFT, command=self.closeTab)
        menu.tk_popup(event.x_root, event.y_root, 0)

    def closeTab(self, event=None):
        id = self.notebook.index(self.notebook.select())
        self.notebook.forget(id)

        try:
            x = len(self.notebook.tabs()) - 1
            self.notebook.select(x)
            self.tabChanged()
        except:
            self.textPad = None
            return


###################################################################
class CreateToolTip():
    """
    create a tooltip for a given widget
    -> this solution was found on stackoverlow.com :)
    """

    def __init__(self, widget, text='widget info'):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 1
        y += self.widget.winfo_rooty() + 40

        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#000000", foreground='#5252FF',
                         relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


###################################################################


if __name__ == '__main__':
    root = tk.Tk()
    app = NotebookFrame(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
