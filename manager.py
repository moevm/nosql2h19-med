import tkinter as tk
import frames
from pandastable import Table, TableModel


class Manager:
    def __init__(self, IMAGE_PATH, WIDTH, HEIGTH):
        print("I'm manager!!")

        self.root = tk.Tk()
        self.root.geometry('{}x{}'.format(WIDTH, HEIGTH))

        self.header = frames.HeaderFrames(self.root, color="#0099ff")
        self.bkrgframe = frames.BkgrFrame(self.root, IMAGE_PATH, WIDTH, HEIGTH)

        self.container = self.bkrgframe.createContainer(20, WIDTH, HEIGTH)

        self.t1 = frames.TableFrame(self.container)
        self.container.insert(self.t1)

        # self.df = TableModel.getSampleData()
        # self.t1 = Table(self.container, dataframe=self.df)#, showtoolbar=True, showstatusbar=True)
        # self.container.insert(self.t1)
        # self.t1.show()

        # self.container.insert(self.t1)

        # self.t1

    def run(self):
        self.root.mainloop()
