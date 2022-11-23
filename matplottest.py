# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

#make sure to import: 'py -m pip install matplotlib', and
#;py -m pip install ./downloads/SomeProject-1.0.4.tar.gz' (whatever the file path is for the .tar.gz file is) in windows+run: cmd
# 'pip install scikit-kinematics'
#also install, numpy, scipy, matplotlib, pandas, sympy, easygui

                    # For Arduino Serial Connection
import numpy as np                  # Scientific computing library for Python
import math                         # For degree calcs, etc
import matplotlib                   # Matplot for the GUI                  
import matplotlib.pyplot as plt                 
import matplotlib.animation as animation
from matplotlib import style
from pylab import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import serial   
import tkinter as tk                # For the GUI interface
from tkinter import ttk
from tkinter import *

# Additional uses here
matplotlib.use("TkAgg")
style.use('ggplot')

##### Some globals
bDebugMode = True
nReadCount_Total = 0
nReadCount_Good = 0
nReadCount_Bad = 0
NUM_IMUS = 4
xar = []
yar12 = []
yar23 = []
yar34 = []

#  Setup the gui globally
LARGE_FONT= ("Verdana", 12)
style.use("ggplot")
f = Figure(figsize=(2,5), dpi=100)
a = f.add_subplot(221)
b = f.add_subplot(222)
c = f.add_subplot(223)

# Init the arrays
##bDebugMode  = True
##NUM_IMUS    = 4
##xar         = []
##yar12       = []
##yar23       = []
##yar34       = []
##
###nReadCount_Total = 0
##nReadCount_Good  = 0
##nReadCount_Bad   = 0

#
#
#FUNCTION: animate::  Control the real time animation to the screen
#
#
def animate(i):#animate data real time
    readArd(NUM_IMUS)
    
    a.clear()
    b.clear()
    c.clear()
    a.plot(xar, yar12)
    b.plot(xar, yar23)
    c.plot(xar, yar34)
#
#
#FUNCTION: readQuats::  Process the raw data from the serial port read procss.  Save to an array
#
#
def readQuats(decodedline):
    splitQs = decodedline.split()#imu 1, would be first 4, imu2 would be second 4, imu 3 would be third 4...
    splitQs = [eval(i) for i in splitQs]
    return splitQs
#
#
#FUNCTION: calcAngle::  Get the angle between quats
#
#
def calcAngle(quat1, quat2):
    insideAC = abs(quat1[0]*quat2[0]+quat1[1]*quat2[1]+quat1[2]*quat2[2]+quat1[3]*quat2[3])
    #If insideAC is > 1, round back down to 1
    if(insideAC > 1):
        insideAC = 1
        
    angle = math.degrees(2*math.acos(insideAC))
    return angle
#
#
#FUNCTION: MakeRotMat:: Make the rotation matrix
#
#
def makeRotMat(quat):
    rotmat = [3][3]
    rotmat = [[quat[0]^2+quat[1]^2-quat[2]^2-quat[3]^2, 2*quat[1]*quat[2]-2*quat[0]*quat[3],2*quat[1]*quat[3]+2*quat[0]*quat[2]], 
    [2*quat[1]*quat[2]+2*quat[0]*quat[3], quat[0]^2-quat[1]^2+quat[2]^2-quat[3]^2, 2*quat[2]*quat[3] - 2*quat[0]*quat[1]],
    [2*quat[1]*quat[3]-2*quat[0]*quat[2], 2*quat[2]*quat[3]+2*quat[0]*quat[1], quat[0]^2-quat[1]^2-quat[2]^2+quat[3]^2]]
    return rotmat;
#
#
#CLASS: SeaofBTCApp:: Manage the GUI and Tkinter
#
#
class SeaofBTCapp(tk.Tk): #for the GUI

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="favicon.ico")
        tk.Tk.wm_title(self, "Team 201 Interface Test")
        #Setup the display        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #Create frames array
        self.frames = {}
        #Init the frames/pages
        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        #Show the starting page
        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
    def show():
        label.config( text = clicked.get() )

#
#
#CLASS: StartPage:: Starting page of the GUI
#
#
        
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

#
#
#CLASS: PageOne:: Container for all the graphs
#
#
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

#
#
#CLASS: PageTwo:: Future page for other display options/graphs
#
#
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
#
#
#CLASS: PageThree:: Future page for other display options/graphs
#
#
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
#
#
#CLASS: PlacedIMU:: Future class for managing the IMUs
#
#       
class placedIMU:
    def __init__(self, position):
        self.position = position
#
#
#FUNCTION:: readArd:: Read from the arduino serial port
#
#
def readArd(numIMU):
    global nReadCount_Good
    global nReadCount_Bad
    global nReadCount_Total
    global bDebugMode
    global xar
    global yar12
    global yar23
    global yar34
#Test to clear the array to see if response is faster
##    if (len(xar)>100):
##        xar.clear()
##    if (len(yar12)>100):
##        yar12.clear()
##    if (len(yar23)>100):
##        yar23.clear()
##    if (len(yar34)>100):
##        yar34.clear()
#End test
    timetot = 0
    #nReadCount_Total += 1
    
    data = arduino.readline().strip().decode("utf-8")
    if(bDebugMode):
        print("Raw Serial Read: ", data)

    allIMU = readQuats(data)
    #if(bDebugMode)
        #print(allIMU)
        #print(len(allIMU))
    
    if(len(allIMU)==(numIMU*4+1)):

        #Update our read count stats
        nReadCount_Good  += 1

        timetot = allIMU[0]/(1000000)
        quat1 = [allIMU[1], allIMU[2], allIMU[3], allIMU[4]]
        quat2 = [allIMU[5], allIMU[6], allIMU[7], allIMU[8]]
        quat3 = [allIMU[9], allIMU[10], allIMU[11], allIMU[12]]
        quat4 = [allIMU[13], allIMU[14], allIMU[15], allIMU[16]]
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
        #no need to return if these are globals. Look into using pass by reference
        #return [xar, yar12, yar23, yar34] 
    else:
              
        #Update our read count stats
        nReadCount_Bad   += 1
              
        if(bDebugMode):
            print("Raw Serial Read: Not enough data...")
        
        if(len(xar) > 0):
            curtime = timetot+xar[len(xar)-1]
            #xar.append(curtime)
        else:
            xar.append(timetot)
            yar12.append(-400)
            yar23.append(-400)
            yar34.append(-400)
        
        # return [xar, yar12, yar23, yar34] #Return of these values not needed since globally defined
    if(nReadCount_Total % 10 ==0):
        print("Total Reads: ", nReadCount_Total)
        print(" Good Reads: ", nReadCount_Good)
        print("  Bad Reads: ", nReadCount_Bad)

#
# Start of main loop
#              
#Open the serial port..Close, then reopen to avoid any init errros (Python issue??)
arduino = serial.Serial(port='COM10', baudrate=115200)
arduino.close()
arduino.open()
print("Serial Port successfully opened...")
app = SeaofBTCapp()     #Init/Start BTC APp
ani = animation.FuncAnimation(f, animate, interval=50)  #Loop 10x a second
app.mainloop()
