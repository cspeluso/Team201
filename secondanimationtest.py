import tkinter
import time
import math
r = 0
anglist = []



# width of the animation window
animation_window_width=800
# height of the animation window
animation_window_height=600
# initial x position of the ball
animation_ball_start_xpos = 50
# initial y position of the ball
animation_ball_start_ypos = 50
# radius of the ball
animation_ball_radius = 30
# the pixel movement of ball for each iteration
animation_ball_min_movement = 5
# delay between successive frames in seconds
animation_refresh_seconds = 0.01

#read file
def readfile(filename):
    file1 = open(filename, "r")
    content = file1.readlines()
    for line in content:
        print(line)
        r = math.radians(float(line));
        anglist.append(r)
    return anglist
# The main window of the animation
def create_animation_window():
  window = tkinter.Tk()
  window.title("Tkinter Animation Demo")
  # Uses python 3.6+ string interpolation
  window.geometry(f'{animation_window_width}x{animation_window_height}')
  return window
 
# Create a canvas for animation and add it to main window
def create_animation_canvas(window):
  canvas = tkinter.Canvas(window)
  canvas.configure(bg="white")
  canvas.pack(fill="both", expand=True)
  return canvas
 
# Create and animate ball in an infinite loop
def animate_ball(window, canvas,xinc,yinc):
  anglist = readfile('C:\\Users\\cathe\\Documents\\externalreviewtest.txt');  
  ball1 = canvas.create_line(500, 300, 300, 300, fill = "red")
  
  ball = canvas.create_line(500,300,300,300,fill="blue")
  count = 0;
  while True:
    r = anglist[count]
    opp = 150*math.sin(r)
    #canvas.move(ball,opp,opp)
    canvas.coords(ball, 500, 300, 300, 300+opp)
    window.update()
    time.sleep(animation_refresh_seconds)
    ball_pos = canvas.coords(ball)
    count+=1;
    # unpack array to variables
    xl,yl,xr,yr = ball_pos
    if xl < abs(xinc) or xr > animation_window_width-abs(xinc):
      xinc = -xinc
    if yl < abs(yinc) or yr > animation_window_height-abs(yinc):
      yinc = -yinc
 
# The actual execution starts here

animation_window = create_animation_window()
animation_canvas = create_animation_canvas(animation_window)
animate_ball(animation_window,animation_canvas, animation_ball_min_movement, animation_ball_min_movement)
