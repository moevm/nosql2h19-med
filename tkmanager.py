import tkinter as tk
import frames
from pandastable import Table, TableModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg# , NavigationToolbar2TkAgg


class tkManager:
    def __init__(self, IMAGE_PATH, WIDTH, HEIGTH):
        print("I'm manager!!")

        self.root = tk.Tk()
        self.root.geometry('{}x{}'.format(WIDTH, HEIGTH))

        self.container = None

        self.header = frames.HeaderFrames(self.root, color="#0099ff", click=lambda opt: self.clik(opt))
        self.header.pack(side=tk.TOP)

        self.bkrgframe = frames.BkgrFrame(self.root, IMAGE_PATH, WIDTH, HEIGTH)
        self.bkrgframe.pack(side=tk.BOTTOM)

        self.container = self.bkrgframe.createContainer(20, WIDTH, HEIGTH)

        self.t1 = frames.TableFrame(self.container)
        self.p1 = frames.PlotFrame(self.container)
        self.frrec = frames.RecFrame(self.container)
        self.imp = frames.ImportExportFrame(self.container,self.imp,"Import")
        self.exp = frames.ImportExportFrame(self.container,self.exp,"Export")
        self.stat = frames.StatFrame(self.container,click=lambda opt:self.clik(opt))
        self.comm = frames.CommonStatFrame(self.container)

    def setbd(self, gman):
        self.gman = gman

    def clik(self, opt):
        if self.container is None:
            print("Init?" + opt)
            return

        if opt == "Import":
            self.container.replace_with(self.imp)
            print("im Import")

        if opt == "Export":
            self.container.replace_with(self.exp)
            print("im Export")

        if opt == "Recogniser":
            self.container.replace_with(self.frrec)
            print("im Recogniser")

        if opt == "Statistics":
            self.container.replace_with(self.stat)
            print("im Statistics")

        if opt == "Graph":
            self.container.replace_with(self.p1)
            print("im Graph")

        if opt == "BDStat":
            self.container.replace_with(self.comm)
            print("im BDStat")



    def imp(self):
        print("im importing!")

    def exp(self):
        print("im exporting!")


    def run(self):
        self.root.mainloop()
