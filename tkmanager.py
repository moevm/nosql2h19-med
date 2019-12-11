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
        self.search_sym = {}
        self.search_dia = {}

        self.header = frames.HeaderFrames(self.root, color="#0099ff", click=lambda opt: self.clik(opt))
        self.header.pack(side=tk.TOP)

        self.bkrgframe = frames.BkgrFrame(self.root, IMAGE_PATH, WIDTH, HEIGTH)
        self.bkrgframe.pack(side=tk.BOTTOM)

        self.container = self.bkrgframe.createContainer(0, WIDTH, HEIGTH)

        self.t1 = frames.TableFrame(self.container)
        self.p1 = frames.PlotFrame(self.container)
        self.frrec = frames.RecFrame(self.container, self.do_search, selected_sym=self.search_sym)
        self.ief = frames.ImportExportFrame(self.container, self.do_imp, self.do_exp)
        self.stat = frames.StatFrame(self.container, click=lambda opt: self.clik(opt), on_submit=self.do_search)
        self.comm = frames.CommonStatFrame(self.container)

    def setbd(self, gman):
        self.gman = gman

    def do_stat(self):
        print("Im doing statistic!")

    def do_search(self, id, tables):
        print("Searching for diagnoses!")
        sym, diag = tables
        str = ""
        frame, type = sym.get_model()
        if type is "Table":
            df = frame.df
            if not df.empty:
                ids = df[df.columns[1]].to_numpy()
                id = np.append(id, ids)
                str = np.array2string(id, separator=" , ")
                data = self.gman.get_sym_via_ids(str)
            else:
                data = self.gman.get_sym_via_ids([id])
            sym.updateData(data)

        frame, type = diag.get_model()
        if type is "Table":
            if str is "":
                data = self.gman.get_diag_via_syd([id])
            else:
                data = self.gman.get_diag_via_syd(str)
            diag.updateData(data)

        if type is "Plot":
            if str is "":
                data = self.gman.get_stat_for_plot([id])
            else:
                data = self.gman.get_stat_for_plot(str)
            names, val = self.process2plot(data)
            val = [i / sum(val) * 100 for i in val]
            print( val )
            diag.updateData(names, val)

    def process2plot(self, data):
        names = [i['Diagnoses'] for i in data]
        val = [i['freq'] for i in data]
        return [names, val]

    def do_BDstat(self):
        pl1, pl2 = self.comm.get_plots()
        data = self.gman.get_BDStat()
        print(data)
        model, type = pl1.get_model()

        model.plot

    def clik(self, opt):
        if self.container is None:
            print("Init?" + opt)
            return

        if opt == "Import/Export":
            self.container.replace_with(self.ief)
            print("im Import and Export")

        if opt == "Recogniser":
            # self.frrec.update_model(self.search_sym)
            self.container.replace_with(self.frrec)
            print("im Recogniser")

        if opt == "Statistics":
            # self.stat.update_model(self.search_sym)
            self.container.replace_with(self.stat)
            print("im Statistics")

        if opt == "Graph":
            self.container.replace_with(self.p1)
            print("im Graph")

        if opt == "BDStat":
            self.do_BDstat()
            self.container.replace_with(self.comm)
            print("im BDStat")

    def do_imp(self, tables):
        if self.gman is None:
            print("Error! No bd manager was found!")
            return 1
        self.gman.load_n_create()
        t1, t2, t3 = tables
        resp = self.gman.loadCSV_dia_t()
        t1.updateData(resp)
        resp = self.gman.loadCSV_sym_t()
        t2.updateData(resp)
        resp = self.gman.loadCSV_dyf()
        print(resp)
        t3.updateData(resp)
        return 0

    def do_exp(self, tables):
        if self.gman is None:
            print("Error! No bd manager was found!")
            return 1
        self.gman.drop_db()
        print("im exporting!")

    def run(self):
        self.root.mainloop()
