from guizero import App, Text, PushButton, Picture, Box, Slider
from brachiograph import BrachioGraph
from linedraw import *
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
from guizero import App
import datetime
import sys
import cv2
from matplotlib import pyplot as plt
import os 
import numpy as np
from PIL import Image

net = cv2.dnn.readNet("yolov3-spp.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# print(classes)
layer_name = net.getLayerNames()
outputlayers = [layer_name[i[0] -1] for i in net.getUnconnectedOutLayers()]

#Generate the amount of specific random colors for each class/type of object detected (numpy array)
colors = np.random.uniform(0, 255, size = (len(classes), 3))


def get_file():
    global fileTime
    #FATAL EXCEPTION TODO: MAKE THE EXE AI WORK WITH OTHER FILE TYPES OTHER THAN JPG 2/20/21 (resolved 2/22/21)
    try:
        orgfile = app.select_file(folder = '/home/pi/BrachioGraph/images/', filetypes=[["JPG File", "*.jpg*"], ["PNG File", "*.png"], ["TIF File", '*.tif*']])
        rawfile = Image.open(orgfile)
        convertedphoto = rawfile.convert("RGB")
        size = len(orgfile)
        fileTime = orgfile[29:size -4]
        convertedphoto.save('/home/pi/BrachioGraph/images/' + fileTime + "_jpgconv.jpg")
        fileTime = fileTime + "_jpgconv"
       # fileTime = convertedphoto[29:size-4]
        print(fileTime)
        text.value = "Current Photo: " + fileTime
        picture.value = convertedphoto

        
    except:
        text.value = "Type Error of Uncaught Exception: A correct file must be selected. Please try again or reselect the removed image"
        print("Unfatal or Uncaught Exception")
        fileTime = None
    
def xchange(x):
    global xrez
    xrez = int(x)

def ychange(y):
    global yrez
    yrez = int(y)

    
def exe():
    global fileTime
    global xrez
    global yrez
    
    time = None
    if xrez == None or yrez == None:
        xrez = 1920
        yrez = 1080
    camera.resolution = (xrez, yrez)
    print(camera.resolution)
    camera.start_preview()
    time =datetime.datetime.now()
    fileTime = str(time)
    print(fileTime)
    sleep(2)    
    camera.capture('/home/pi/BrachioGraph/images/'+ fileTime + ".jpg")   
    picture.value = '/home/pi/BrachioGraph/images/'+ fileTime + ".jpg"
    text.value = "Current Photo Location: '/home/pi/BrachioGraph/images/'"+ fileTime + ".jpg. Press the Convert button to convert. "
    
def convert():
    global fileTime
    if fileTime == None:
        text.value = "Please Take a Picture Before Conversion"
    else:
        dir__image = cv2.imread("/home/pi/BrachioGraph/images/"+ fileTime + ".jpg")
        print(dir__image.shape)
        scale_percent = 200

        #calculate the scale percent of original dimensions
        width = int(dir__image.shape[1] * scale_percent / 100)
        height = int(dir__image.shape[0] * scale_percent / 100)
        dsize = (width, height)
        output = cv2.resize(dir__image, dsize)
       # print(output.shape)
        # cv2.imwrite('/home/pi/BrachioGraph/images/' + fileTime + '_resized.jpg',output) 
  
        img = cv2.imread('/home/pi/BrachioGraph/images/' + fileTime + '.jpg')
        img = cv2.resize(img, None, fx = 0.4, fy = 0.4)
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True)

        net.setInput(blob)
        outs = net.forward(outputlayers)
        boxes = []
        confidences = []
        class_ids = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        font = cv2.FONT_HERSHEY_SIMPLEX
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = classes[class_ids[i]]
                confidence_label = confidences[i] * 100
                r_conf = round(confidence_label, 3)
                r_conf = str(r_conf)
                color = colors[i]
                cv2.putText(img, label, (x, y+30), font, 1, color, 2)
                cv2.putText(img, r_conf, (x, y+60), font, 1, color, 2)
                cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)

        cv2.imshow("AI- Common Object Detection : Close this window to continue printing ", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        print(img.shape)
        text.value = "Printing Complete: '/home/pi/BrachioGraph/images/'"+ fileTime + ".jpg. "
        image_to_json(fileTime, draw_contours = 1, draw_hatch = 16)
        #Default draw_contours value = 2. Due to thickness constraints and imperfections it has been tuned down to 1. Vaue = 3 for pencil or light drawings
        GPIO.output(25, GPIO.HIGH)
        bg.plot_file('images/' + fileTime + '.json')
        GPIO.output(25, GPIO.LOW)
def terminate():
    print('Program Executed Safely')
    GPIO.cleanup()
    sys.exit()

    
fileTime = None
xrez = None
yrez = None

bg = BrachioGraph()
camera = PiCamera()
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

GPIO.output(25, GPIO.LOW)

app = App(title = "Brachiograph Manager")
app.warn("Caution Before Proceeding", "This is a python application created by Michael Liu. This was created for a python raspberry pi project with object detection ai modules. This may be slower on some machines. Opimized for lightweight machines.  Clicking OK ensures you understand the application and its capabilities.")
intro = Text(app, text="Brachiograph Manager", size=40, font="Times New Roman", color="black")
text = Text(app, text="BrachioGraph Manager created by Michael Liu")
exe = PushButton(app, command= exe, text="Camera", width = "fill")
getfile = PushButton(app, command = get_file, text = "Import", width = "fill")
convert = PushButton(app, command = convert, text = "Convert", width = "fill")
terminate = PushButton(app, command = terminate, text = "Terminate", width = "fill")


xinfo = Text(app, text = "X-Axis Resolution for Camera")
xslider = Slider(app, start = 640, end = 1920, command = xchange)
yinfo = Text(app, text = "Y-Axis Resolution for Camera")
yslider = Slider(app, start = 480, end = 1080, command = ychange)

justareminder = Text(app, text = 'The current picture to print will show up here:')
picture = Picture(app, image=None)

    
  
    
app.display()
