# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	


#make sure to import: 'py -m pip install matplotlib', and
#;py -m pip install ./downloads/SomeProject-1.0.4.tar.gz' (whatever the file path is for the .tar.gz file is) in windows+run: cmd
# 'pip install scikit-kinematics'
#also install, numpy, scipy, matplotlib, pandas, sympy, easygui


import numpy as np # Scientific computing library for Python
#for the GUI
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
import matplotlib.animation as animation
from matplotlib import style
from pylab import *
style.use('ggplot')
#format for data serial
numIMU = 2
import math

#for data transfer from ard->py
import serial
import time
#arduino = serial.Serial(port='COM10', baudrate=115200)#, timeout=.1)
#def write_read(x):
    #arduino.write(bytes(x, 'utf-8'))

    #time.sleep(0.05)
    #return data
##while True:
##    num = input("Enter a number: ") # Taking input from user
##    value = write_read(num)
##    print(value) # printing the value

#for sci-kinematics


#for the GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


import tkinter as tk
from tkinter import ttk
from tkinter import *

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")
f = Figure(figsize=(2,5), dpi=100)
a = f.add_subplot(221)
b = f.add_subplot(222)
c = f.add_subplot(223)
#d = f.add_subplot(224)
global xar 
global yar12
global yar23
global yar34
xar = []
yar12 = []
yar23 = []
yar34 = []

def animate(i):#animate data real time
    [xar12, yar12, yar23, yar34] = initArd(4)
    #print(yar12)
    #print(yar23)
    #print(yar34)
    a.clear()
    a.plot(xar,yar12)
    b.clear()
    b.plot(xar, yar23)
    c.clear()
    c.plot(xar, yar34)

def readQuats(decodedline):
    splitQs = decodedline.split()#imu 1, would be first 4, imu2 would be second 4, imu 3 would be third 4...
    splitQs = [eval(i) for i in splitQs]
    return splitQs
def readRPY(decodedline):
    splitRPY = decodedline.split()#rpy of 1, then rpy of 2
    splitRPY = [eval(i) for i in splitRPY]
    return splitRPY
def calcAngle(quat1, quat2):
    insideac = abs(quat1[0]*quat2[0]+quat1[1]*quat2[1]+quat1[2]*quat2[2]+quat1[3]*quat2[3])
    #print(abs(quat1[0]*quat2[0]+quat1[1]*quat2[1]+quat1[2]*quat2[2]+quat1[3]*quat2[3]))
    if(insideac > 1):
        insideac = 1;
    elif(insideac <-1):
        insideac = -1
    angle = math.degrees(2*math.acos(insideac))
    return angle
def makeRotMat(quat):
    rotmat = [3][3]
    rotmat = [[quat[0]^2+quat[1]^2-quat[2]^2-quat[3]^2, 2*quat[1]*quat[2]-2*quat[0]*quat[3],2*quat[1]*quat[3]+2*quat[0]*quat[2]], 
    [2*quat[1]*quat[2]+2*quat[0]*quat[3], quat[0]^2-quat[1]^2+quat[2]^2-quat[3]^2, 2*quat[2]*quat[3] - 2*quat[0]*quat[1]],
    [2*quat[1]*quat[3]-2*quat[0]*quat[2], 2*quat[2]*quat[3]+2*quat[0]*quat[1], quat[0]^2-quat[1]^2-quat[2]^2+quat[3]^2]]
    return rotmat;
def rpyDataToAbsAngle():
    arduino = serial.Serial(port='COM11', baudrate=115200)#, timeout=.1)
    while True:
        data = arduino.readline().decode()
        print("hello!")
        print(data)
        bothIMU = readRPY(data)
        print(bothIMU)
        #print(bothIMU)
        quat1 = get_quaternion_from_euler(bothIMU[1], bothIMU[2], bothIMU[3])
        quat2 = get_quaternion_from_euler(bothIMU[4], bothIMU[5], bothIMU[6])
        #print(calcAngle(quat1, quat2))
def quatsToAngle():
    while True:
        data = arduino.readline().decode()
        #print(data)
        bothIMU = readQuats(data)
        print(calcAngle(bothIMU[0:4], bothIMU[4:]))
        rotmat1 = makeRotMat(bothIMU[0:4])
        #print(rotmat1)
#! /usr/bin/env python3
 
# This program converts Euler angles to a quaternion.
# Author: AutomaticAddison.com
def get_quaternion_from_euler(roll, pitch, yaw):
  """
  Convert an Euler angle to a quaternion.
   
  Input
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.
 
  Output
    :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
  """
  qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
  qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
  qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
 
  return [qx, qy, qz, qw]
 
  

class SeaofBTCapp(tk.Tk): #for the GUI

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="favicon.ico")
        tk.Tk.wm_title(self, "Team 201 Interface Test")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
    def show():
        label.config( text = clicked.get() )

        
class StartPage(tk.Frame): #for the GUI

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()


class PageOne(tk.Frame): #for the GUI
    
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x = 1100, y = 30)

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.place(x = 1100, y = 60)
    
      
        # Dropdown menu options
        options = [
            "Punch",
            "Kick",
            "Roundhouse Kick",
            "Twist"
        ]
      
    # datatype of menu text
        clicked = StringVar()
      
    # initial menu text
        clicked.set( "Punch" )
      
    # Create Dropdown menu
        drop = OptionMenu( self , clicked , *options )
        drop.place(x=30, y=30)
      
##    # Create button, it will change label text
##        button = Button( self , text = "click Me" , command = controller.show ).pack()
##      
##    # Create Label
##        label = Label( self , text = " " )
##        label.pack()
        

        canvas = FigureCanvasTkAgg(f, self)
        #canvas.show()
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        thismanager = get_current_fig_manager()
        thismanager.window.wm_geometry("+2000+200")
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        

##        canvas = FigureCanvasTkAgg(f, self) ##commented out for animation test, works fine for static graph
##        canvas.draw()
##        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
##
##        toolbar = NavigationToolbar2Tk(canvas, self)
##        toolbar.update()
##        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageTwo(tk.Frame): #for the GUI

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame): #for the GUI

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f1 = Figure(figsize=(5,5), dpi=100)
        a = f1.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        

        canvas = FigureCanvasTkAgg(f1, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
class placedIMU:
    def __init__(self, position):
        self.position = position
def initArd(numIMU):
    #arduino = serial.Serial(port='COM10', baudrate=115200) #timeout=.1)
    #arduino.close()
    #arduino.open()
    #while True:
        #data = arduino.readline().decode()
    timetot = 0
    data = arduino.readline().strip().decode("utf-8")
    print(data)
    allIMU = readQuats(data)
    print(allIMU)
    print(len(allIMU))
    if(len(allIMU)==(numIMU*4+1)):
        timetot = allIMU[0]/(1000000)
        quat1 = [allIMU[1], allIMU[2], allIMU[3], allIMU[4]]
        quat2 = [allIMU[4], allIMU[5], allIMU[6], allIMU[7]]
        quat3 = [allIMU[8], allIMU[9], allIMU[10], allIMU[11]]
        quat4 = [allIMU[12], allIMU[13], allIMU[14], allIMU[15]]
        absangle12 = calcAngle(quat1, quat2);
        absangle23 = calcAngle(quat2, quat3);
        absangle34 = calcAngle(quat3, quat4);
        if(len(xar)>0):
            curtime = timetot+xar[len(xar)-1]
            xar.append(curtime)
            #print(xar)
        else:
            xar.append(timetot)
            
        yar12.append(absangle12)
        yar23.append(absangle23)
        yar34.append(absangle34)
        
        return [xar, yar12, yar23, yar34]
    else:
        print("not enough")
        
        if(len(xar) > 0):
            curtime = timetot+xar[len(xar)-1]
            #xar.append(curtime)
        else:
            xar.append(timetot)
            yar12.append(-400)
            yar23.append(-400)
            yar34.append(-400)
##        print(xar)
##        print(yar12)
##        print(yar23)
##        print(yar34)
        
        return [xar, yar12, yar23, yar34]
        
    
#rpyDataToAbsAngle()
arduino = serial.Serial(port='COM10', baudrate=115200)
arduino.close()
arduino.open()

app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
