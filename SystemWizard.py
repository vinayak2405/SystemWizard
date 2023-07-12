from tkinter import *
from tkinter import ttk , messagebox
import tkinter as tk
from tkinter import filedialog
import platform
import psutil

#brightness
import screen_brightness_control as pct

#audio
from ctypes import cast , POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume

# weather
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

# clock
from time import strftime

# calendar
from tkcalendar import *

#open file managar
import subprocess 

# open google
import webbrowser as wb

import random

import pyautogui as autogui

# camera
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import PIL.Image, PIL.ImageTk
import os


# painttt 
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image



root = Tk()
root.title('SystemWizard')

root.geometry("850x500+300+170")
root.resizable(False , False)
root.configure(bg = '#292e2e')

# #icon 
image_icon = PhotoImage(file="Image/icon.png")
root.iconphoto(False , image_icon)

Body = Frame(root , width=900 , height=600 , bg = "#d6d6d6" )
Body.pack(pady=20,padx=20)

#-----------------------------------------

LHS = Frame(Body , width=310 , height = 435 , bg="#f4f5f5" , highlightbackground="#adacb1" , highlightthickness = 1)
LHS.place(x = 10 , y = 10)

#logo
photo = PhotoImage(file="Image/laptop.png")
myimage = Label(LHS , image = photo , background="#f4f5f5")
myimage.place(x = 2 , y =20)

my_system = platform.uname()

l1 = Label(LHS , text = f"{my_system.node}'s laptop", bg = "#f4f5f5" , font = ('Acumin Variable Concept' , 15 , 'bold') , justify="center")   #can change name from here
l1.place(x = 20 , y = 200)

l2 = Label(LHS , text = f"Version:{my_system.version}" , bg = "#f4f5f5" , font = ('Acumin Variable Concept' , 8) , justify="center")  
l2.place(x = 20 , y = 225) 

l3 = Label(LHS , text = f"System:{my_system.system}" , bg = "#f4f5f5" , font = ('Acumin Variable Concept' , 15) , justify="center")   
l3.place(x = 20 , y = 250) 

l4 = Label(LHS , text = f"Machine:{my_system.machine}" , bg = "#f4f5f5" , font = ('Acumin Variable Concept' , 15) , justify="center")   
l4.place(x = 20 , y = 285) 

l5 = Label(LHS , text = f"Total RAM installed:{round(psutil.virtual_memory().total/1000000000,2)} GB" , bg = "#f4f5f5" , font = ('Acumin Variable Concept' , 13) , justify="center")   
l5.place(x = 20 , y = 320) 

l6 = Label(LHS , text = f"Processor:{my_system.processor}" , bg = "#f4f5f5" , font = ('Acumin Variable Concept' , 5) , justify="center")   
l6.place(x = 20 , y = 345) 
#-----------------------------------------

RHS = Frame(Body , width=470 , height = 230 , bg="#f4f5f5" , highlightbackground="#adacb1" , highlightthickness = 1)
RHS.place(x = 330 , y = 10)

system = Label(RHS , text = "System" , font = ("Acumin Variable Concept" , 15) , bg = "#f4f5f5")
system.place(x=10 , y=10)


##############################battery##############################

def convertTime (seconds):
    minutes, seconds=divmod(seconds, 60)
    hours, minutes=divmod(minutes, 60)
    return "%d:%02d:%02d"% (hours, minutes, seconds)

# def convertTime(seconds):
#     minutes, seconds = divmod(seconds, 60)
#     hours, minutes = divmod(minutes, 60)
#     days, hours = divmod(hours, 24)
#     return f"{days}:{hours:02d}:{minutes:02d}:{seconds:02d}"


def none():
    global battery_png
    global battery_label
    battery = psutil.sensors_battery()
    percent = battery.percent
    time = convertTime(battery.secsleft)

    lbl.config(text=f"{percent}%")
    lbl_plug.config(text=f"Plug in:{str(battery.power_plugged)}")
    lbl_time.config(text=f"{time} remaining")
    # print(percent)
    # print(time)

    battery_label=Label(RHS, background= '#f4f5f5')
    battery_label.place(x=15,y=50)
    
    lbl.after(1000,none)
    
    if battery.power_plugged==True:
        battery_png=PhotoImage(file="Image/charging.png")
        battery_label.config(image=battery_png)
    else:
        battery_png=PhotoImage(file='Image/battery.png')
        battery_label.config(image=battery_png)



lbl = Label(RHS , font = ("Acumin Variable Concept" , 40 , "bold") , bg = "#f4f5f5")
lbl.place(x=200 , y=30)

lbl_plug = Label(RHS , font = ("Acumin Variable Concept" , 10) , bg = "#f4f5f5")
lbl_plug.place(x=20 , y=100)

lbl_time = Label(RHS , font = ("Acumin Variable Concept" , 15) , bg = "#f4f5f5")
lbl_time.place(x=200 , y=110)

none() 

###################################################################

############################speaker################################

lbl_speaker=Label(RHS, text= "Speaker:",font=('arial' ,10, 'bold'),bg="#f4f5f5")
lbl_speaker.place(x=10,y=150)
volume_value=tk.DoubleVar()

def get_current_volume_value():
    return '{: .2f}'. format(volume_value.get())

def volume_changed(event):
    device =AudioUtilities. GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-float(get_current_volume_value()),None)


style= ttk.Style()
style.configure("TScale", background= '#f4f5f5')

volume=ttk.Scale(RHS, from_=60, to=0, orient= 'horizontal', command=volume_changed, variable=volume_value)
volume.place(x=90,y=150)
volume.set(20)


################################Brightness#################################

lbl_brightness=Label(RHS, text= 'Brightness' ,font=('arial',10, 'bold'),bg="#f4f5f5")
lbl_brightness.place(x=10,y=190)

current_value=tk.DoubleVar()

def get_current_value():
    return '{: .2f}'.format(current_value.get())

def brightness_changed(event):
    pct.set_brightness(get_current_value())

brightness= ttk.Scale(RHS, from_=0,to=100, orient= 'horizontal', command=brightness_changed, variable=current_value)
brightness.place(x=90,y=190)




################################################################################

################################Weather####################################

def weather(): 
    app1=Toplevel()
    app1.geometry('850x500+300+170')
    app1.title('Weather')
    app1.configure (bg='#f4f5f5')
    app1.resizable (False, False)

    #icon
    image_icon=PhotoImage(file='Image/App1.png')
    app1.iconphoto (False,image_icon) 
    
    def getWeather():
        try:
            city=textfield.get()
            geolocator= Nominatim (user_agent="geoapi Exercises")
            location=geolocator.geocode(city)
            obj= TimezoneFinder()
            result = obj.timezone_at (lng=location. longitude, lat=location. latitude)
            
            home=pytz.timezone(result)
            local_time=datetime.now(home)
            current_time=local_time.strftime("%I: %M %p")
            clock.config(text=current_time)
            name.config(text="CURRENT WEATHER")

            #weather
            api="https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=646824f2b7b86caffec1d0b16ea77f79"
            json_data = requests.get(api).json()
            
            condition = json_data['weather'][0]['main']
            description = json_data['weather'][0]['description']
            temp = int(json_data['main']['temp']-273.15)
            pressure = json_data[ 'main']['pressure']
            humidity= json_data['main']['humidity']
            wind= json_data[ 'wind' ]['speed']

            t.config(text=(temp,"°"))
            c.config(text=(condition,"|","FEELS","LIKE", temp, '°'))

            w.config(text=wind)
            h.config(text=humidity)
            d.config(text=description) 
            p.config(text=pressure)


        except Exception as e:
            messagebox.showerror("Weather App","Invalid Entry")

    
    #search box
    Search_image=PhotoImage(file="Image/search.png")
    myimage=Label (app1, image=Search_image, bg="#f4f5f5")
    myimage.place(x=20, y=20)
    textfield=tk.Entry (app1, justify='center',width=17, font=('poppins', 25, 'bold') , bg = '#404040' , fg = "white")
    textfield.place(x = 50 , y = 35)
    textfield.focus()

    Search_icon=PhotoImage(file="Image/search_icon.png")
    myimage_icon=Button(app1, image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040",command=getWeather)
    myimage_icon.place(x=400, y=33)
    
    #logo
    Logo_image=PhotoImage(file="Image/logo.png")
    logo=Label (app1, image=Logo_image, bg="#f4f5f5")
    logo.place(x=160, y=120)
    
    #bottom box
    Frame_image=PhotoImage(file="Image/box.png") 
    frame_myimage=Label (app1, image=Frame_image, bg="#f4f5f5")
    frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

    #time
    name=Label (app1, font=('arial', 15, 'bold'),bg="#f4f5f5")
    name.place(x=30, y=100)
    clock=Label(app1, font=('Helvetica',20), bg="#f4f5f5")
    clock.place(x=30, y=130) 

    #label
    label1=Label (app1, text="WIND", font=("Helvatica", 15, 'bold'), fg="white", bg="#1ab5ef")
    label1.place(x=95, y=400)
    label2=Label (app1, text="HUMIDITY", font=("Helvatica", 15, 'bold'), fg="white", bg="#1ab5ef")
    label2.place(x=220, y=400)
    label3=Label(app1, text="DESCRIPTION", font=("Helvatica", 15, 'bold'), fg="white", bg="#1ab5ef")
    label3.place(x=400, y=400)
    label4=Label (app1, text="PRESSURE", font=("Helvatica", 15, 'bold'), fg="white", bg="#1ab5ef")
    label4.place(x=630, y=400)
    t=Label(app1, font=('arial', 70, 'bold'),fg="#ee666d", bg='#f4f5f5')
    t.place(x=400, y=130)
    
    c=Label (app1, font=('arial', 15, 'bold' ), bg='#f4f5f5')
    c.place(x=400, y=250)

    w=Label (app1, text="...", font=('arial', 12, 'bold'), bg="#1ab5ef")
    w.place(x=105, y=430)
    h=Label(app1, text="...", font=('arial', 12, 'bold'), bg="#1ab5ef")
    h.place(x=260, y=430)
    d=Label(app1, text="..." ,font=('arial', 12, 'bold'), bg="#1ab5ef")
    d.place(x=420, y=430)
    p=Label(app1, text="..." ,font=('arial', 12, 'bold'), bg="#1ab5ef")
    p.place(x=670, y=430)

    app1.mainloop()

########################clock#######################################

def clock():
    app2=Toplevel()
    app2.geometry("850x110+300+10")
    app2.title('Clock')
    app2.configure(bg="#292e2e")
    app2.resizable(False, False)
    
    #icon
    image_icon=PhotoImage(file="Image/App2.png")
    app2.iconphoto(False,image_icon) 
    
    def clock():
        text=strftime('%H:%M:%S %p')
        lbl.config(text=text)
        lbl.after (1000, clock)
    
    lbl=Label (app2, font=('digital-7', 50, 'bold'), width=20, bg="#f4f5f5",fg="#292e2e")
    lbl.pack (anchor='center', pady=20)
    clock()

    app2.mainloop()

##########################################calendar##########################################################

def calendar():
    app3=Toplevel()
    app3.geometry ("300x300+-10+10")
    app3.title('Calendar')
    app3.configure (bg="#292e2e")
    app3.resizable (False, False) 
    
    #icon
    image_icon=PhotoImage(file="Image/App3.png")
    app3.iconphoto (False,image_icon)
    mycal=Calendar (app3, setmode= 'day', date_pattern='d/m/yy')
    mycal.pack(padx=15 , pady=35)
    
    app3.mainloop()

#######################################blcakandwhite#############################################

button_mode = True

def mode():
    global button_mode
    if button_mode:
        LHS.config(bg="#292e2e")
        myimage.config(bg="#292e2e")
        
        l1.config(bg="#292e2e", fg="#d6d6d6")
        l2.config(bg="#292e2e", fg="#d6d6d6")
        l3.config(bg="#292e2e", fg="#d6d6d6")
        l4.config(bg="#292e2e", fg="#d6d6d6")
        l5.config(bg="#292e2e", fg="#d6d6d6")
        l6.config(bg="#292e2e", fg="#d6d6d6")
        RHB.config(bg="#292e2e")
        app1.config(bg="#292e2e")
        app2.config(bg="#292e2e")
        app3.config(bg="#292e2e")
        app4.config(bg="#292e2e")
        app5.config(bg="#292e2e")
        app6.config(bg="#292e2e")
        app7.config(bg="#292e2e")
        app8.config(bg="#292e2e")
        app9.config(bg="#292e2e")
        app10.config(bg="#292e2e")
        apps.config(bg="#292e2e", fg="#d6d6d6")
        button_mode = False

    else:
        LHS.config(bg="#f4f5f5")
        myimage.config(bg="#f4f5f5")
        
        l1.config(bg="#f4f5f5" , fg="#292e2e")
        l2.config(bg="#f4f5f5" ,fg="#292e2e")
        l3.config(bg="#f4f5f5", fg="#292e2e")
        l4.config(bg="#f4f5f5" , fg="#292e2e")
        l5.config(bg="#f4f5f5" , fg="#292e2e")
        l6.config(bg="#f4f5f5" , fg="#292e2e")

         

        RHB.config(bg="#f4f5f5")
        app1.config(bg="#f4f5f5")
        app2.config(bg="#f4f5f5")
        app3.config(bg="#f4f5f5")
        app4.config(bg="#f4f5f5")
        app5.config(bg="#f4f5f5")
        app6.config(bg="#f4f5f5")
        app7.config(bg="#f4f5f5")
        app8.config(bg="#f4f5f5")
        app9.config(bg="#f4f5f5")
        app10.config(bg="#f4f5f5") 

        apps.config(bg="#f4f5f5", fg="#292e2e")

        button_mode = True

#####################################game#########################################################

def game():
    app5=Toplevel()
    app5.geometry("420x470+1152+170")
    #root.minsize(700,500)
    #root.maxsize(700,500)
    app5.title("Tic Tac Toe")

    # X starts so true
    clicked=True
    count=0

    #rest function..
    def reset():
        global b1,b2,b3,b4,b5,b6,b7,b8,b9
        global clicked,count
        clicked=True
        count=0

    # disable all the buttons
    def disable_all_buttons():
        b1.config(state=DISABLED)
        b2.config(state=DISABLED)
        b3.config(state=DISABLED)
        b4.config(state=DISABLED)
        b5.config(state=DISABLED)
        b6.config(state=DISABLED)
        b7.config(state=DISABLED)
        b8.config(state=DISABLED)
        b9.config(state=DISABLED)

    # Check to see if someone won
    def checkiwon():
        global winner
        winner=False

        if b1["text"] == "X" and b2["text"] == "X" and b3["text"] =="X":
            b1.config(bg="red")
            b2.config(bg="red")
            b3.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! X Wins!!")
            disable_all_buttons()

        elif b4["text"] == "X" and b5["text"] == "X" and b6["text"] =="X":
            b4.config(bg="red")
            b5.config(bg="red")
            b6.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! X Wins!!")
            disable_all_buttons()

        elif b7["text"] == "X" and b8["text"] == "X" and b9["text"] =="X":
            b7.config(bg="red")
            b8.config(bg="red")
            b9.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! X Wins!!")
            disable_all_buttons()

        elif b1["text"] == "X" and b4["text"] == "X" and b7["text"] =="X":
            b1.config(bg="red")
            b4.config(bg="red")
            b7.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! X Wins!!")
            disable_all_buttons()

        elif b2["text"] == "X" and b5["text"] == "X" and b8["text"] =="X":
            b2.config(bg="red")
            b5.config(bg="red")
            b8.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! X Wins!!")
            disable_all_buttons()

        elif b3["text"] == "X" and b6["text"] == "X" and b9["text"] =="X":
            b3.config(bg="red")
            b6.config(bg="red")
            b9.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! X Wins!!")
            disable_all_buttons()

        elif b1["text"] == "X" and b5["text"] == "X" and b9["text"] =="X":
            b1.config(bg="red")
            b5.config(bg="red")
            b9.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! X Wins!!")
            disable_all_buttons()

        elif b3["text"] == "X" and b5["text"] == "X" and b7["text"] =="X":
            b3.config(bg="red")
            b5.config(bg="red")
            b7.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! X Wins!!")
            disable_all_buttons()

            ### CHECK FOR O'S WINS


        elif b1["text"] == "O" and b2["text"] == "O" and b3["text"] =="O":
            b1.config(bg="red")
            b2.config(bg="red")
            b3.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! O Wins!!")
            disable_all_buttons()

        elif b4["text"] == "O" and b5["text"] == "O" and b6["text"] =="O":
            b4.config(bg="red")
            b5.config(bg="red")
            b6.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! O Wins!!")
            disable_all_buttons()

        elif b7["text"] == "O" and b8["text"] == "O" and b9["text"] =="O":
            b7.config(bg="red")
            b8.config(bg="red")
            b9.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! O Wins!!")
            disable_all_buttons()

        elif b1["text"] == "O" and b4["text"] == "O" and b7["text"] =="O":
            b1.config(bg="red")
            b4.config(bg="red")
            b7.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! O Wins!!")
            disable_all_buttons()

        elif b2["text"] == "O" and b5["text"] == "O" and b8["text"] =="O":
            b2.config(bg="red")
            b5.config(bg="red")
            b8.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! O Wins!!")
            disable_all_buttons()

        elif b3["text"] == "O" and b6["text"] == "O" and b9["text"] =="O":
            b3.config(bg="red")
            b6.config(bg="red")
            b9.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! O Wins!!")
            disable_all_buttons()

        elif b1["text"] == "O" and b5["text"] == "O" and b9["text"] =="O":
            b1.config(bg="red")
            b5.config(bg="red")
            b9.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! O Wins!!")
            disable_all_buttons()

        elif b3["text"] == "O" and b5["text"] == "O" and b7["text"] =="O":
            b3.config(bg="red")
            b5.config(bg="red")
            b7.config(bg="red")
            winner=True
            messagebox.showinfo("Tic Tac Toe","CONGRATULATIONS! O  Wins!!")
            disable_all_buttons()


    def b_click(b):
        global clicked,count
        
        if b["text"] ==" " and clicked==True:
            b["text"]="X"
            clicked=False
            count+=1
            checkiwon()

        elif b["text"] ==" " and clicked==False:
            b["text"]="O"
            clicked=True
            count+=1
            checkiwon()

        elif count == 9:
            messagebox.showwarning("Tic Tac Toe","Draw!")

        else:
            messagebox.showerror("Tic Tac Toe","Hey! That box has already been selected\npick Another Box....")


    

    b1=Button(app5,text=" ",font=("Helvetica",20),height=3,width=6,bg="SystemButtonFace",command=lambda: b_click(b1))
    b2=Button(app5,text=" ",font=("Helvetica",20),height=3,width=6,bg="SystemButtonFace",command=lambda: b_click(b2))
    b3=Button(app5,text=" ",font=("Helvetica",20),height=3,width=6,bg="SystemButtonFace",command=lambda: b_click(b3))

    b4=Button(app5,text=" ",font=("Helvetica",20),height=3,width=6,bg="SystemButtonFace",command=lambda: b_click(b4))
    b5=Button(app5,text=" ",font=("Helvetica",20),height=3,width=6,bg="SystemButtonFace",command=lambda: b_click(b5))
    b6=Button(app5,text=" ",font=("Helvetica",20),height=3,width=6,bg="SystemButtonFace",command=lambda: b_click(b6))

    b7=Button(app5,text=" ",font=("Helvetica",20),height=3,width=6,bg="SystemButtonFace",command=lambda: b_click(b7))
    b8=Button(app5,text=" ",font=("Helvetica",20),height=3,width=6,bg="SystemButtonFace",command=lambda: b_click(b8))
    b9=Button(app5,text=" ",font=("Helvetica",20),height=3,width=6,bg="SystemButtonFace",command=lambda: b_click(b9))

    #Grid our buttons to the screen.......
    b1.grid(row=0,column=0)
    b2.grid(row=0,column=1)
    b3.grid(row=0,column=2)

    b4.grid(row=1,column=0)
    b5.grid(row=1,column=1)
    b6.grid(row=1,column=2)

    b7.grid(row=2,column=0)
    b8.grid(row=2,column=1)
    b9.grid(row=2,column=2)

    # Create menu
    my_menu=Menu(app5)
    app5.config(menu=my_menu)

    # Create options menu
    options_menu=Menu(my_menu,tearoff=False)
    my_menu.add_cascade(label="options",menu=options_menu)################################################################################
    options_menu.add_command(label='Reset Game',command=reset)
    reset()

    app5.mainloop()

######################################screenshot##################################################

def Screenshot():
    app6 = Toplevel()
    app6.title('Screenshot')

    class CameraApp:
        def __init__(self, master):
            self.master = master
            self.video_capture = None
            self.photo = None

            self.create_widgets()

        def create_widgets(self):
            self.btn_open_camera = tk.Button(self.master, text="Open Camera", command=self.open_camera)
            self.btn_open_camera.pack(pady=10)

            self.btn_capture_photo = tk.Button(self.master, text="Capture Photo", command=self.capture_photo, state=tk.DISABLED)
            self.btn_capture_photo.pack(pady=5)

            self.btn_exit = tk.Button(self.master, text="Exit", command=self.master.quit)
            self.btn_exit.pack(pady=10)

            self.lbl_photo = tk.Label(self.master)
            self.lbl_photo.pack(pady=10)

        def open_camera(self):
            video_device_index = 0  # Change this if your camera is not the default device

            # Open the video capture
            self.video_capture = cv2.VideoCapture(video_device_index)

            # Check if the video capture is successfully opened
            if not self.video_capture.isOpened():
                messagebox.showerror("Error", "Failed to open the camera.")
                return

            self.btn_open_camera.configure(state=tk.DISABLED)
            self.btn_capture_photo.configure(state=tk.NORMAL)

            self.show_camera_feed()

        def show_camera_feed(self):
            _, frame = self.video_capture.read()

            if frame is not None:
                # Convert the frame from BGR to RGB for displaying in tkinter
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Resize the frame to fit the label
                height, width, _ = frame_rgb.shape
                image = PIL.Image.fromarray(frame_rgb)
                image = image.resize((int(width / 2), int(height / 2)))

                # Create a PhotoImage and update the label
                self.photo = PIL.ImageTk.PhotoImage(image=image)
                self.lbl_photo.configure(image=self.photo)

            # Schedule the next frame update
            self.master.after(1, self.show_camera_feed)

        def capture_photo(self):
            # Read a frame from the camera
            _, frame = self.video_capture.read()

            # Generate a unique filename for the captured photo
            filename = "photo.jpg"
            index = 1
            while os.path.exists(filename):
                filename = f"photo{index}.jpg"
                index += 1

            # Save the frame as a photo
            cv2.imwrite(filename, frame)

            messagebox.showinfo("Capture Photo", f"Photo saved as {filename}.")

    CameraApp(app6)
    app6.mainloop()

#######################################file#####################################################

def file():
    subprocess. Popen (r'explorer /select, "C:\path\of\folder\file"')

#####################################crome##############################################

def crome():
    wb.register('chrome', None)
    wb.open('https://www.google.com/')

##################################paint################################################

def paint_app():

    
    
    class Paint(object):

        app9 = Toplevel()
        app9.title("Paint")
        app9.geometry("670x500+1152+170")

        DEFAULT_PEN_SIZE = 5.0
        DEFAULT_COLOR = 'black'

        def __init__(self):
            
            # self.app9.maxsize(500,300)
            # self.app9.minsize(500,300)
        
            self.paint_tools = Frame(self.app9,width=100,height=300,relief=RIDGE,borderwidth=2 )
            self.paint_tools.place(x=0,y=0)

            self.pen_logo = ImageTk.PhotoImage(file=('Image/pen.png'))
            self.p = Label(self.paint_tools, text="pen",borderwidth=0,font=('verdana',10,'bold'))
            self.p.place(x=5,y=11)
            self.pen_button = Button(self.paint_tools,padx=6,image=self.pen_logo,borderwidth=2,command=self.use_pen)
            self.pen_button.place(x=60,y=10)

            self.brush_logo = ImageTk.PhotoImage(file=('Image/brush.png'))
            self.b = Label(self.paint_tools,borderwidth=0,text='brush',font=('verdana',10,'bold'))
            self.b.place(x=5,y=40)
            self.brush_button = Button(self.paint_tools,image = self.brush_logo,borderwidth=2,command=self.use_brush) 
            self.brush_button.place(x=60,y=40)

            self.color_logo = ImageTk.PhotoImage(file=('Image/color.png'))
            self.cl = Label(self.paint_tools, text='color',font=('verdana',10,'bold'))
            self.cl.place(x=5,y=70)
            self.color_button = Button(self.paint_tools,image = self.color_logo,borderwidth=2,command=self.choose_color)
            self.color_button.place(x=60,y=70)

            self.eraser_logo = ImageTk.PhotoImage(file=('Image/eraser.png'))
            self.e = Label(self.paint_tools, text='eraser',font=('verdana',10,'bold'))
            self.e.place(x=5,y=100)
            self.eraser_button = Button(self.paint_tools,image = self.eraser_logo,borderwidth=2,command=self.use_eraser)
            self.eraser_button.place(x=60,y=100)

            self.pen_size = Label(self.paint_tools,text="Pen Size",font=('verdana',10,'bold'))
            self.pen_size.place(x=8,y=250)
            self.choose_size_button = Scale(self.paint_tools, from_=1, to=10, orient=VERTICAL)
            self.choose_size_button.place(x=20,y=150)
            

            self.c = Canvas(self.app9, bg='white', width=600, height=600,relief=RIDGE,borderwidth=0)
            self.c.place(x=100,y=0)



            self.setup()
            self.app9.mainloop()


        def setup(self):
            self.old_x = None
            self.old_y = None
            self.line_width = self.choose_size_button.get()
            self.color = self.DEFAULT_COLOR
            self.eraser_on = False
            self.active_button = self.pen_button
            self.c.bind('<B1-Motion>', self.paint)
            self.c.bind('<ButtonRelease-1>', self.reset)

        def use_pen(self):
            self.activate_button(self.pen_button)

        def use_brush(self):
            self.activate_button(self.brush_button)

        def choose_color(self):
            self.eraser_on = False
            self.color = askcolor(color=self.color)[1]

        def use_eraser(self):
            self.activate_button(self.eraser_button, eraser_mode=True)

        def activate_button(self, some_button, eraser_mode=False):
            self.active_button.config(relief=RAISED)
            some_button.config(relief=SUNKEN)
            self.active_button = some_button
            self.eraser_on = eraser_mode

        def paint(self, event):
            self.line_width = self.choose_size_button.get()
            paint_color = 'white' if self.eraser_on else self.color
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                width=self.line_width, fill=paint_color,
                                capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.old_x = event.x
            self.old_y = event.y

        def reset(self, event):
            self.old_x, self.old_y = None, None


    if __name__ == '__main__':
            Paint()

    
    # app9=Paint(app9)
   
    
        
####################################################################################

def notebook():
    app10 = Toplevel()
    app10.geometry("700x580+1152+170")
    class NoteTakingApp:
        
        
        def __init__(self, master):
            self.master = master
            master.title("Note Taking App")

            self.text_widget = tk.Text(master)
            self.text_widget.pack()

            self.save_button = tk.Button(master, text="Save", command=self.save_file)
            self.save_button.pack()

            self.load_button = tk.Button(master, text="Load", command=self.load_file)
            self.load_button.pack()

            self.clear_button = tk.Button(master, text="Clear", command=self.clear_text)
            self.clear_button.pack()

        def save_file(self):
            file_path = filedialog.asksaveasfilename(defaultextension=".txt")
            with open(file_path, "w") as f:
                f.write(self.text_widget.get("1.0", "end"))

        def load_file(self):
            file_path = filedialog.askopenfilename()
            with open(file_path, "r") as f:
                self.text_widget.delete("1.0", "end")
                self.text_widget.insert("1.0", f.read())

        def clear_text(self):
            self.text_widget.delete("1.0", "end")

    
    NoteTakingApp(app10)
    app10.mainloop()
    


############################################################################
#-----------------------------------------

RHB= Frame(Body , width=470 , height = 190 , bg="#f4f5f5" , highlightbackground="#adacb1" , highlightthickness = 1)
RHB.place(x = 330, y = 255)

apps=Label(RHB, text='Apps',font=('Acumin Variable Concept', 15), bg='#f4f5f5')
apps.place(x=10, y=10)

app1_image=PhotoImage(file='Image/App1.png')
app1=Button (RHB, image=app1_image, bd=0 , command=weather)
app1.place(x=15, y=50)

app2_image=PhotoImage(file='Image/App2.png')
app2=Button (RHB, image=app2_image, bd=0 , command=clock)
app2.place(x=100, y=50)

app3_image=PhotoImage(file='Image/App3.png')
app3=Button (RHB, image=app3_image, bd=0 , command=calendar)
app3.place(x=185, y=50)

app4_image=PhotoImage(file='Image/App4.png')
app4=Button (RHB, image=app4_image, bd=0 , command=mode)
app4.place(x=270, y=50)

app5_image=PhotoImage(file='Image/tttq.png' )
app5=Button (RHB, image=app5_image, bd=0 , command=game)
app5.place(x=355, y=50)

app6_image=PhotoImage(file='Image/App6.png')
app6=Button (RHB, image=app6_image, bd=0 , command=Screenshot)
app6.place(x=15, y=120)

app7_image=PhotoImage(file='Image/App7.png')
app7=Button (RHB, image=app7_image, bd=0 , command=file)
app7.place(x=100,y=120)

app8_image=PhotoImage(file='Image/App8.png')
app8=Button (RHB, image=app8_image, bd=0 , command=crome)
app8.place(x=185, y=120)

app9_image=PhotoImage (file='Image/paint1.png')    
app9=Button (RHB, image=app9_image, bd=0 , command=paint_app)
app9.place(x=270,y=120)

app10_image=PhotoImage (file='Image/appnote.png')
app10=Button (RHB, image=app10_image, bd=0 , command=notebook)
app10.place(x=355, y=120)



root.mainloop()