import time
from time import monotonic
import jetson.inference
import jetson.utils
from SerialCommand import Com

s = Com(ARDPath = "/dev/ttyUSB0", portSpeed = 115200)
#s.writeCmd_(128)

coefficient = 1
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource("/dev/video1")
display = jetson.utils.videoOutput("display://0")
t = None

while display.IsStreaming():
    img = camera.Capture()
    detections = net.Detect(img)
    person = None
    person_Area = 0
    for i in detections:
        if(i.ClassID==1):
            if(i.Area>person_Area):
                person = i
                person_Area = i.Area
    b = 0
    coefficient = 1
    if(person):
        t = None
        if(person.Center[0]>350):
            coefficient = (person.Center[0] - 320)/320
            b = -20
        elif(person.Center[0]<290):
            coefficient = (320 - person.Center[0])/320
            b = 20
    else:
        if(t == None):
            t = monotonic()
        if(monotonic()-t>10):
            b = 127
        else:
            b = 0
    if (b != 127):
        b = int(coefficient*b)
    com = 128 + b
    s.writeCmd_(com)
    time.sleep(0.1)
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
