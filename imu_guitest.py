import tkinter as tk
from tkinter import *
import math
import time

file1 = open('C:\\Users\\cathe\\Downloads\\AngleTestRunNoTime.txt', "r")
content = file1.readlines()

# Variable for storing the sum
r = 0
anglist = []
# Iterating through the content
# Of the file
root = tk.Tk()
##Window = tk.Tk()
##Window.geometry(f'500x500')
canv = Canvas(root, width = 400, height = 250)

canv.pack()
x1 = canv.create_line(150, 200, 300, 200, fill = "blue")
for line in content:
    print(line)
    r = math.radians(float(line));
    anglist.append(r)
            
   
    opp = 150*math.sin(r)
    #message = tk.Label(root, text="Hello, World!")
    #message.pack()


    #x2 = canv.create_line(150, 200, 300, 200+opp, fill = "red")
    #root.after(200, canv.create_line(150, 200, 300, 200+opp, fill = "red"))
opp = 150*math.sin(anglist[1])
x2 = canv.create_line(150, 200, 300, 200+opp, fill = "red")
for i in anglist:
    opp = 150*math.sin(i)
    canv.move(x2, 300,200+opp)
    time.sleep(0.2)
    #x2 = canv.create_line(150, 200, 300, 200+opp, fill = "red")
    canv.pack()
root.mainloop()    



