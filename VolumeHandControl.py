import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2
import time
import numpy as np
import HandTrackingModule as htm
###########################################
wcam,hcam=640,480
###########################################


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()

minVol=volrange[0]
maxVol=volrange[1]

cam=cv2.VideoCapture(0)
cam.set(3,wcam)
cam.set(4,hcam)
ptime=0


detector=htm.handDetector(detectionCon=0.8)
volPer=0
volBar=400
while True:
    success,img=cam.read()
    img=detector.findHands(img)
    mylist=[]
    mylist=detector.findPosition(img,draw=False)
    if len(mylist)!=0:
        x1=mylist[4][1]
        y1=mylist[4][2]
        x2=mylist[8][1]
        y2=mylist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),10,(255,255,0),cv2.FILLED)
        cv2.circle(img, (x2, y2),10,(255,255,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,120,255),4)
        cv2.circle(img, (cx, cy), 10, (255, 120, 0), cv2.FILLED)
        distance=math.hypot(x2-x1,y2-y1)
        # print(int(distance))
        vol = np.interp(distance, [50,200], [minVol, maxVol])
        volBar=np.interp(distance,[50,200],[400,100])
        volPer=np.interp(distance,[50,200],[0,100])
        volume.SetMasterVolumeLevel(vol, None)

        if(distance<50):
            cv2.circle(img, (cx, cy),10,(123,255,0),cv2.FILLED)

        # print(int(distance),vol)
    cv2.rectangle(img,(50,100),(65,400),(255,0,0),3)
    cv2.rectangle(img, (50, int(volBar)), (65, 400),(255,0,0),cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (50,450), cv2.FONT_HERSHEY_COMPLEX, 1,
                (255, 0, 0), 3)
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f'FPS:{int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,1,
                (255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)