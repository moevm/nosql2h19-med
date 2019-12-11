from PIL import Image, ImageTk

from tkmanager import *
from bdmanager import *

if __name__ == '__main__':
    IMAGE_PATH = './appdata/background.jpg'
    WIDTH, HEIGTH = 1500, 800

    m = tkManager(IMAGE_PATH, WIDTH, HEIGTH)

    GRAPH = "http://localhost:7474/"

    bd = bdManager(GRAPH, True)

    m.setbd(bd)

    m.run()
