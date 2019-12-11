from PIL import Image, ImageTk
import tkinter as tk
from pandastable import Table, TableModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # , NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import pandas as pd


class BkgrFrame(tk.Frame):
    def __init__(self, parent, file_path, width, height):
        super(BkgrFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.canvas = tk.Canvas(self, width=width, height=height)
        pil_img = Image.open(file_path)
        self.img = ImageTk.PhotoImage(pil_img.resize((width, height), Image.ANTIALIAS))
        self.bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        self.canvas.pack()

        self.pack(side=tk.BOTTOM)

    def add(self, widget, x, y):
        self.canvas_window = self.canvas.create_window(x, y, anchor=tk.NW, window=widget)

    def createContainer(self, pad, width, height):
        container = Container(self, width - 2 * pad, height - 2 * pad)
        self.canvas.create_window(pad, pad, anchor=tk.NW, window=container)
        return container


class HeaderFrames(tk.Frame):
    def __init__(self, parent, color, click):
        super(HeaderFrames, self).__init__(parent, borderwidth=0, highlightthickness=0, background=color, )

        self.COLOR = color

        self.label = tk.Label(self, bg=self.COLOR, text='Symptom and Diagnosis')
        self.label.pack()

        self.btn = []
        self.btn.append(tk.Button(self, bg=self.COLOR, text="Import/Export", command=lambda: click("Import/Export")))
        # self.btn.append(tk.Button(self, bg=self.COLOR, text="Export", command=lambda: click("Export")))
        self.btn.append(tk.Button(self, bg=self.COLOR, text="Recogniser", command=lambda: click("Recogniser")))
        self.btn.append(tk.Button(self, bg=self.COLOR, text="Statistics", command=lambda: click("Statistics")))
        self.btn.append(tk.Button(self, bg=self.COLOR, text="Graph", command=lambda: click("Graph")))

        for b in self.btn:
            b.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.pack(side=tk.TOP, fill=tk.X)


class Container(tk.Frame):
    def __init__(self, parent, width, height):
        super(Container, self).__init__(parent, borderwidth=0,
                                        highlightthickness=0)  # , width=width, height=height - 50)
        width = width
        height = height - 50

        self.content = None

        # self.pack()

    def replace_with(self, frame):
        if self.content is not None:
            self.content.forget()
        self.content = frame
        self.content.pack()


class TableFrame(tk.Frame):
    """Basic test frame for the table"""

    # http: // dmnfarrell.github.io / pandastable /
    def __init__(self, parent, width=400, height=500, ):
        super(TableFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)
        self.table = pt = Table(self, width=width, height=height)
        pt.show()

    def updateData(self, data):
        model = TableModel(pd.DataFrame.from_records(data))
        self.table.updateModel(model)
        self.table.redraw()
        print("Modifing some data")

    def get_model(self):
        # print(self.table.model)
        return self.table.model


class PlotFrame(tk.Frame):
    def __init__(self, parent=None):
        super(PlotFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def putdata(self, data):
        print("Putting new plot")


class RecFrame(tk.Frame):
    def __init__(self, parent, on_submit, selected_sym={}, related_diag={}):
        super(RecFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.label1 = tk.Label(self, text="Ch00se your symptoms")
        self.label1.grid(row=0, column=0)

        self.entry = tk.Entry(self)
        self.entry.grid(row=1, column=0)
        self.entry.bind("<Key>", lambda event: self.submit(event))

        self.btn = tk.Button(self, text="Submit", command=lambda: self.submit())
        self.btn.grid(row=1, column=1)

        self.sellab = tk.Label(self, text="Selected sympt")
        self.sellab.grid(row=2, column=0)

        self.seltb = TableFrame(self,340,400)
        self.seltb.grid(row=3, column=0)
        self.seltb.updateData(selected_sym)

        self.label2 = tk.Label(self, text="Related Diagnoses")
        self.label2.grid(row=0, column=2)

        self.diagtb = TableFrame(self,340,400)
        self.diagtb.grid(row=3, column=2)
        self.diagtb.updateData(related_diag)

        self.update = on_submit

    def submit(self, e=None):
        if e is not None:
            if e.keycode != 13:
                return
        id = self.entry.get()
        self.entry.delete(0, tk.END)
        self.update(id, self.get_tables())

    def get_tables(self):
        return [self.seltb, self.diagtb]


class ImportExportFrame(tk.Frame):
    def __init__(self, parent, clickImp, clickExp, width=345, height=400):
        super(ImportExportFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.t1 = TableFrame(self, width=width, height=height)
        self.t1.grid(row=0, column=0)

        self.t2 = TableFrame(self, width=width, height=height)
        self.t2.grid(row=0, column=1)

        self.t3 = TableFrame(self, width=width, height=height)
        self.t3.grid(row=0, column=2)

        self.btnImp = tk.Button(self, text="Import", command=lambda: clickImp(self.get_tables()))
        self.btnImp.grid(row=1, column=0)

        self.btnExp = tk.Button(self, text="Export", command=lambda: clickExp(self.get_tables()))
        self.btnExp.grid(row=1, column=1)

    def get_tables(self):
        return [self.t1, self.t2, self.t3]


class StatFrame(tk.Frame):
    def __init__(self, parent, click):
        super(StatFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.label1 = tk.Label(self, text="Ch00se your symptoms")
        self.label1.grid(row=0, column=0)

        self.entry = tk.Entry(self)
        self.entry.grid(row=1, column=0)

        self.btn = tk.Button(self, text="Submit")
        self.btn.grid(row=1, column=1)

        self.sellab = tk.Label(self, text="Selected sympt")
        self.sellab.grid(row=2, column=0)

        self.seltb = TableFrame(self)
        self.seltb.grid(row=3, column=0)

        self.plot = PlotFrame(self)
        self.plot.grid(row=3, column=3)

        self.statbtn = tk.Button(self, text="Statistic", command=lambda: click("BDStat"))
        self.statbtn.grid(row=4, column=3)


class CommonStatFrame(tk.Frame):
    def __init__(self, parent):
        super(CommonStatFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)

        self.l1 = tk.Label(self, text="The most fr symptoms")
        self.l1.grid(row=0, column=1)

        self.l2 = tk.Label(self, text="The least diagnosable diagnoses")
        self.l2.grid(row=0, column=2)

        self.plot1 = PlotFrame(self)
        self.plot1.grid(row=1, column=1)

        self.plot2 = PlotFrame(self)
        self.plot2.grid(row=1, column=2)

# app = TableFrame()
# launch the app
# app.mainloop()
