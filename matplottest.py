# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/	

#make sure to import: 'py -m pip install matplotlib', and
#;py -m pip install ./downloads/SomeProject-1.0.4.tar.gz' (whatever the file path is for the .tar.gz file is) in windows +run: cmd
# 'pip install scikit-kinematics'
#also install, numpy, scipy, matplotlib, pandas, sympy, easygui, csv


                    # For Arduino Serial Connection
import numpy as np                  # Scientific computing library for Python
import math
import time
# For degree calcs, etc
import matplotlib                   # Matplot for the GUI                  
import matplotlib.pyplot as plt                 
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib import style
from pylab import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import serial   
import tkinter as tk                # For the GUI interface
from tkinter import ttk
from tkinter import *
import csv 

# Additional uses here
matplotlib.use("TkAgg")
style.use('ggplot')

##### Some globals
bDebugMode = True
bTogArd = True
nReadCount_Total = 0
nReadCount_Good = 0
nReadCount_Bad = 0
NUM_IMUS = 8
xar = []
yarShould_L = []
yarShould_L_2 = []
yarHip_L = []
yarHip_L_2 = []
yarKnee_L = []
yarKnee_L_2 = []
yarShould_R = []
yarShould_R_2 = []
yarHip_R = []
yarHip_R_2 = []
yarKnee_R = []
yarKnee_R_2 = []
instruct = False
#trial mumber
trialCounter = 1
loopCount = 0
bStored = False


#  Setup the gui globally
LARGE_FONT= ("Verdana", 12)
style.use("ggplot")


f = Figure(figsize=(2,5), dpi=100)
a = f.add_subplot(221)
b = f.add_subplot(222)
c = f.add_subplot(223)
d = f.add_subplot(224)

    
##axback = f.add_axes([0.7, 0.05, 0.1, 0.075])
##bnext = Button(axback, 'Back')
##bnext.on_clicked(plt.hide())

#FUNCTION: animate::  Control the real time animation to the screen
#
#
##def animate(i):#animate data real time
##    loopArd(NUM_IMUS)
##    
##    a.clear()
##    b.clear()
##    c.clear()
##    a.plot(xar, yar12)
##    b.plot(xar, yar23)
##    c.plot(xar, yar34)
    
def loopArd():
    global trialCounter
    global loopCount
    xar.clear()
    if instruct:
        yarShould_L_2.clear()
        yarHip_L_2.clear()
        yarKnee_L_2.clear()
        yarShould_R_2.clear()
        yarHip_R_2.clear()
        yarKnee_R_2.clear()
    else:
        yarShould_L.clear()
        yarHip_L.clear()
        yarKnee_L.clear()
        yarShould_R.clear()
        yarHip_R.clear()
        yarKnee_R.clear()
        
    initSec = time.time()
    bStored = False
    while(time.time() - initSec < 10): #loops arduino for 10 seconds
        readArd(NUM_IMUS)
    print(loopCount)
    write2File()    
    #add trial counter
    trialCounter +=1
    

    
#
#
#FUNCTION: readQuats::  Process the raw data from the serial port read procss.  Save to an array
#
#

def write2File():
    global instruct
    writeFile = open('C:\\Users\\cathe\\Documents\\vvtrial_3_1213.csv', 'w', newline='')
    # create the csv writer
    writer = csv.writer(writeFile)
    # write a row to the csv file
    writeFile.write("trial number:")
    writeFile.write(str(trialCounter))
    writer.writerow("")
    writeFile.write("time, left shoulder, right shoulder, left hip, right hip, left knee, right knee")
    writer.writerow("")
    for i in range(len(xar)):
##        print(i)
##        print(len(yarKnee_L))
##        print(len(yarHip_L))
##        print(len(yarShould_L))
##        print(len(yarKnee_R))
##        print(len(yarHip_R))
##        print(len(yarShould_R))
##        print(len(xar))
        if instruct:
            thisrow = [xar[i], yarShould_L_2[i], yarShould_R_2[i], yarHip_L_2[i], yarHip_R_2[i], yarKnee_L_2[i], yarKnee_R_2[i]]
        else:
            thisrow = [xar[i], yarShould_L[i], yarShould_R[i], yarHip_L[i], yarHip_R[i], yarKnee_L[i], yarKnee_R[i]]
        writer.writerow(thisrow)
    # close the file
    writeFile.close()
    print("file written")
    writeFile.close()
    bStored = True
    
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
    insideAC = abs(quat1[0]*quat2[0]+quat1[1]*-quat2[1]+quat1[2]*-quat2[2]+quat1[3]*-quat2[3])
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
    def fullCyc(self):
        global loopCount
        print("HELLO")
        loopCount = 0
        if bTogArd:
            loopArd()
            #initPlot()
            bStored = True
            
    

    
        
#
#CLASS: StartPage:: Starting page of the GUI
#
#
    
class StartPage(tk.Frame): #for the GUI

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Welcome to Motion Capture", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Start Session",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

##        button2 = ttk.Button(self, text="Visit Page 2",
##                            command=lambda: controller.show_frame(PageTwo))
##        button2.pack()
##
##        button3 = ttk.Button(self, text="Graph Page",
##                            command=lambda: controller.show_frame(PageThree))
##        button3.pack()

#
#
#CLASS: PageOne:: Container for all the graphs
#
#
class PageOne(tk.Frame): #for the GUI
    
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.place(x = 1100, y = 20)

        button2 = ttk.Button(self, text="Start Capture",
                            command=lambda: controller.fullCyc())
        button2.place(x = 500, y = 20)

        button4 = ttk.Button(self, text = "Student Trial", command = lambda: self.instructfal())
        button4.place(x = 300, y = 20)
        
        button4 = ttk.Button(self, text = "Instructor Trial", command = lambda: self.instructtru())
        button4.place(x = 400, y = 20)
        
        button3 = ttk.Button(self, text = "Plot", command = lambda: self.showPlot())
        button3.place(x = 600, y = 20)

        label = tk.Label(self, text="*Plot after both student and instructor trials are taken*", font=LARGE_FONT)
        label.pack(pady=70,padx=40)
        
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

       
    def showPlot(self):
        a.clear()
        b.clear()
        c.clear()
        d.clear()
        if len(yarShould_R) > len(yarShould_R_2):
            for i in range(len(yarShould_R) - len(yarShould_R_2)):
                yarShould_R_2.append(0)
                yarHip_R_2.append(0)
                yarKnee_R_2.append(0)
                yarShould_L_2.append(0)
                yarHip_L_2.append(0)
                yarKnee_L_2.append(0)
        if len(yarShould_R) < len(yarShould_R_2):
            for i in range(len(yarShould_R_2) - len(yarShould_R)):
                yarShould_R.append(0)
                yarHip_R.append(0)
                yarKnee_R.append(0)
                yarShould_L.append(0)
                yarHip_L.append(0)
                yarKnee_L.append(0)
        print(len(yarShould_R))
        print(len(yarShould_R_2))
        a.plot(xar, yarShould_R)
        a.plot(xar, yarShould_R_2)
        b.plot(xar, yarHip_R)
        b.plot(xar, yarHip_R_2)
        c.plot(xar, yarShould_L)
        c.plot(xar, yarShould_L_2)
        d.plot(xar, yarKnee_R)
        d.plot(xar, yarKnee_R_2)
        a.title.set_text('right should')
        b.title.set_text('right hip')
        c.title.set_text('left shoulder')
        d.title.set_text('right knee')
        canvas = FigureCanvasTkAgg(f, self)
        #canvas.show()
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)  
        # Dropdown menu options

    def instructtru(self):
        global instruct
        instruct = True
    def instructfal(self):
        global instruct
        instruct = False

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
    global loopCount
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
    #print(data)
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
        quatarm_R = [allIMU[1], allIMU[2], allIMU[3], allIMU[4]] #0
        quatarm_L = [allIMU[5], allIMU[6], allIMU[7], allIMU[8]] #1
        quathip_R = [allIMU[9], allIMU[10], allIMU[11], allIMU[12]] #2
        quathip_L = [allIMU[13], allIMU[14], allIMU[15], allIMU[16]] #3
        quatthigh_R = [allIMU[17], allIMU[18], allIMU[19], allIMU[20]]
        quatthigh_L = [allIMU[21], allIMU[22], allIMU[23], allIMU[24]]
        quatshin_R =[allIMU[21], allIMU[22], allIMU[23], allIMU[24]]
        quatshin_L = [allIMU[21], allIMU[22], allIMU[23], allIMU[24]]
        
        
        aaShould_L = calcAngle(quatarm_L, quathip_L);
        aaShould_R = calcAngle(quatarm_R, quathip_R);
        aaHip_L = calcAngle(quatthigh_L, quathip_L);
        aaHip_R = calcAngle(quatthigh_R, quathip_R);
        aaKnee_L = calcAngle(quatthigh_L, quatshin_L);
        aaKnee_R = calcAngle(quatthigh_R, quatshin_R);

        if(len(xar)>0):
            curtime = timetot+xar[len(xar)-1]
            xar.append(curtime)
        else:
            xar.append(timetot)
        if instruct:
            yarShould_L_2.append(aaShould_L)
            yarShould_R_2.append(aaShould_R)
            yarHip_L_2.append(aaHip_L)
            yarHip_R_2.append(aaHip_R)
            yarKnee_L_2.append(aaKnee_L)
            yarKnee_R_2.append(aaKnee_R)
        else:
            yarShould_L.append(aaShould_L)
            yarShould_R.append(aaShould_R)
            yarHip_L.append(aaHip_L)
            yarHip_R.append(aaHip_R)
            yarKnee_L.append(aaKnee_L)
            yarKnee_R.append(aaKnee_R)
        loopCount+=1
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
            yarShould_R.append(-400)
            yarHip_R.append(-400)
            yarKnee_R.append(-400)
        
        # return [xar, yar12, yar23, yar34] #Return of these values not needed since globally defined
    if(nReadCount_Total % 10 ==0 and bDebugMode):
        print("Total Reads: ", nReadCount_Total)
        print(" Good Reads: ", nReadCount_Good)
        print("  Bad Reads: ", nReadCount_Bad)

#
# Start of main loop
#              
#Open the serial port..Close, then reopen to avoid any init errros (Python issue??)
if(bTogArd):
    arduino = serial.Serial(port='COM17', baudrate=115200)
    arduino.close()
    arduino.open()
    print("Serial Port successfully opened...")
else:
    print("Toggle Arduino: Off")
app = SeaofBTCapp()     #Init/Start BTC App
##if(bTogArd):
##    ani = animation.FuncAnimation(f, animate, interval=10)  #Loop 10x a second
app.mainloop()
