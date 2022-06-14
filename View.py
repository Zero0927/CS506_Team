import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import numpy as np 
from SnapchatFilter import *

my_w = tk.Tk()
my_w.geometry("700x600")
my_w.minsize(700,600)
my_w.maxsize(700,600)
my_w.title('Snapchat Filter')
my_font1=('times', 18, 'bold')

l1 = tk.Label(my_w,text='Please upload a picture',width=30,font=my_font1)  
l1.grid(row=1,column=1, sticky="ew")


b1 = tk.Button(my_w, text='Upload File', 
   width=20,command = lambda:upload_file())
b1.grid(row=2,column=1,sticky='ew') 

my_w.grid_columnconfigure((0, 4), weight=1)

def upload_file():
    global img
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    
    output = add_hat(filename)
    cv2.imwrite("output.jpg",output)
    
    img=Image.open("output.jpg")
    img=img.resize((600,500))   
    
    img=ImageTk.PhotoImage(image=img)
    
    b2 =tk.Button(my_w,image=img)
    b2.grid(row=3,column=1) 


my_w.mainloop() 
