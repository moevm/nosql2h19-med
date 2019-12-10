from PIL import Image, ImageTk

from tkmanager import *
from bdmanager import *

if __name__ == '__main__':
    IMAGE_PATH = './appdata/background.jpg'
    WIDTH, HEIGTH = 1500, 800

    m = tkManager(IMAGE_PATH, WIDTH, HEIGTH)

    GRAPH = "http://localhost:7474/"

    bd = bdManager(GRAPH, True)

    # resp = bd.loadCSV()

    m.setbd(bd)

    m.run()

    # # Put some tkinter widgets in the BkgrFrame.
    # button1 = bkrgframe.add(tk.Button(root, text="Start"), 10, 10)
    # button2 = bkrgframe.add(tk.Button(root, text="Continue"), 50, 10)

# import tkinter
# import cv2
# import PIL.Image, PIL.ImageTk
#
# # Create a window
# window = tkinter.Tk()
# window.title("OpenCV and Tkinter")
#
# # Load an image using OpenCV
# cv_img = cv2.cvtColor(cv2.imread("./appdata/background.jpg"), cv2.COLOR_BGR2RGB)
#
# # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
# height, width, no_channels = cv_img.shape
#
# # Create a canvas that can fit the above image
# canvas = tkinter.Canvas(window, width = width, height = height)
# canvas.pack()
#
# # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
# photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(cv_img))
#
# # Add a PhotoImage to the Canvas
# canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
#
# # Run the window loop
# window.mainloop()
