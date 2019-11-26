from PIL import Image, ImageTk
import tkinter as tk
from pandastable import Table, TableModel


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
    def __init__(self, parent, color):
        super(HeaderFrames, self).__init__(parent, borderwidth=0, highlightthickness=0, background=color, )

        self.COLOR = color

        self.label = tk.Label(self, bg=self.COLOR, text='Symptom and Diagnosis')
        self.label.pack()

        self.btn = []
        self.btn.append(tk.Button(self, bg=self.COLOR, text="Import"))
        self.btn.append(tk.Button(self, bg=self.COLOR, text="Export"))
        self.btn.append(tk.Button(self, bg=self.COLOR, text="Recogniser"))
        self.btn.append(tk.Button(self, bg=self.COLOR, text="Statistics"))
        self.btn.append(tk.Button(self, bg=self.COLOR, text="Graph"))

        for b in self.btn:
            b.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.pack(side=tk.TOP, fill=tk.X)


class Container(tk.Frame):
    def __init__(self, parent, width, height):
        super(Container, self).__init__(parent, borderwidth=0, highlightthickness=0, width=width, height=height - 50)
        width = width
        height = height - 50

        self.content = None

        self.pack()

    def insert(self, widget):
        print("inserted!!!")
        self.content = widget
        # self.content.pack()


class TableFrame(tk.Frame):
    """Basic test frame for the table"""

    def __init__(self, parent=None):
        super(TableFrame, self).__init__(parent, borderwidth=0, highlightthickness=0)
        self.f = tk.Frame(self)
        self.f.pack(fill=tk.BOTH, expand=1)
        self.df = TableModel.getSampleData()
        self.table = pt = Table(self.f, dataframe=self.df)
        print("i'm table!")
        pt.show()
        self.pack(side=tk.RIGHT)



# app = TableFrame()
# launch the app
# app.mainloop()
