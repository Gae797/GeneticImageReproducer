# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import tkinter as tk
import time

BORDER = 50
FONT_SIZE = 24

root = None
img_1 = None
img_2 = None
label_1 = None
label_2 = None
pipe = None

def openImage(path, size):
    
    target = Image.open(path)
    target = target.resize((size, size))
    channels = target.split()
    
    return target, channels
    
def mergeChannels(red, green, blue):
    
    return np.dstack((red,green,blue))
    
def pixelsToImage(pixels):
        
    return Image.fromarray(pixels.astype('uint8'), 'RGB')

def createWindow(image, target, resize):
    
    global root, img_1, img_2, label_2
    
    root = tk.Tk()
    root.title("Comparison")
    root.geometry("{}x{}".format(resize*2 + BORDER*3,resize + BORDER*3))
    
    tk_img_1 = ImageTk.PhotoImage(target.resize((resize,resize)))
    img_1 = tk.Label(root, image=tk_img_1)
    img_1.pack()
    img_1.place(x=BORDER,y=BORDER)
    
    tk_img_2 = ImageTk.PhotoImage(image.resize((resize,resize)))
    img_2 = tk.Label(root, image=tk_img_2)
    img_2.pack()
    img_2.place(x=resize + BORDER*2,y=BORDER)
    
    label_1 = tk.Label(text="Original", font=("Courier", FONT_SIZE))
    label_1.pack()
    label_1.place(x=BORDER + 100, y=resize + BORDER*2 - 25)
    
    label_2 = tk.Label(text="Generation: 0", font=("Courier", FONT_SIZE))
    label_2.pack()
    label_2.place(x=resize + BORDER*2 + 30, y=resize + BORDER*2 - 25)
    
    root.lift()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)
    
    root.after(100,updateWindow, resize)
    root.mainloop()
    
def updateWindow(resize):
    
    global root, img_2, label_2
    
    if pipe:
        
        if pipe[-1]==None:
            time.sleep(5)
            root.destroy()
            return
        
    try:
            red, green, blue, generation = pipe.pop(0)
            pixels = mergeChannels(red, green, blue)
            _image = pixelsToImage(pixels)
            _image = ImageTk.PhotoImage(_image.resize((resize,resize)))
            
            img_2.configure(image=_image)
            img_2.image=_image
            
            label_2.configure(text = "Generation: {}".format(generation))
            
            root.update()
    except:
        pass
        
    root.after(100,updateWindow, resize)
    
def display(_pipe, target, resize):
    
    global pipe
    pipe = _pipe
    red, green, blue, generation = pipe.pop(0)
    pixels = mergeChannels(red, green, blue)
    image = pixelsToImage(pixels)
    
    createWindow(image, target, resize)
    
def plot(values, x_label, y_label, optimal):
    
    plt.plot(values)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.axhline(y=optimal)
    plt.show()