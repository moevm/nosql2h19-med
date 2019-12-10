import tkinter as tk
import frames
from pandastable import Table, TableModel
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # , NavigationToolbar2TkAgg
import numpy as np


class tkManager:
    def __init__(self, IMAGE_PATH, WIDTH, HEIGTH):
        print("I'm manager!!")

        self.root = tk.Tk()
        self.root.geometry('{}x{}'.format(WIDTH, HEIGTH))

        self.gman = None
        self.container = None

        self.header = frames.HeaderFrames(self.root, color="#0099ff", click=lambda opt: self.clik(opt))
        self.header.pack(side=tk.TOP)

        self.bkrgframe = frames.BkgrFrame(self.root, IMAGE_PATH, WIDTH, HEIGTH)
        self.bkrgframe.pack(side=tk.BOTTOM)

        self.container = self.bkrgframe.createContainer(0, WIDTH, HEIGTH)

        self.t1 = frames.TableFrame(self.container)
        self.p1 = frames.PlotFrame(self.container)
        self.frrec = frames.RecFrame(self.container, self.do_search)
        self.ief = frames.ImportExportFrame(self.container, self.do_imp, self.do_exp)
        self.stat = frames.StatFrame(self.container, click=lambda opt: self.clik(opt))
        self.comm = frames.CommonStatFrame(self.container)

    def setbd(self, gman):
        self.gman = gman

    def do_search(self, id, tables):
        print("Searching for diagnoses!")
        sym, diag = tables
        df = sym.get_model().df
        if not df.empty:
            ids = df[df.columns[1]].to_numpy()
            id = np.append(id, ids)
            print(id)
            str = np.array2string(id, separator=" , ")
            data = self.gman.get_sym_via_ids(str)
            sym.updateData(data)
        else:
            data = self.gman.get_sym_via_ids([id])
            sym.updateData(data)


    def clik(self, opt):
        if self.container is None:
            print("Init?" + opt)
            return

        if opt == "Import/Export":
            self.container.replace_with(self.ief)
            print("im Import and Export")

        # if opt == "Export":
        #     self.exp.set_tables(self.stf)
        #     self.container.replace_with(self.exp)
        #     print("im Export")

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

    def do_imp(self, tables):
        if self.gman is None:
            print("Error! No bd manager was found!")
            return 1
        self.gman.load_n_create()
        t1, t2, t3 = tables
        resp = self.gman.loadCSV_dia_t()
        # print(resp)
        t1.updateData(resp)
        resp = self.gman.loadCSV_sym_t()
        # print(resp)
        t2.updateData(resp)
        resp = self.gman.loadCSV_dyf()
        print(resp)
        t3.updateData(resp)
        # print("im importing!")
        return 0

    def do_exp(self, tables):
        if self.gman is None:
            print("Error! No bd manager was found!")
            return 1
        self.gman.drop_db()
        print("im exporting!")

    def run(self):
        self.root.mainloop()
