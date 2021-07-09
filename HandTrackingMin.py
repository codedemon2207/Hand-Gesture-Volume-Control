import cv2
import mediapipe as mp
import time

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
mpHand=mp.solutions.hands
hands=mpHand.Hands()
mpdraw=mp.solutions.drawing_utils

pTime,cTime=0,0
while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handlmrk in results.multi_hand_landmarks:
            for id,lm in enumerate(handlmrk.landmark):
                # print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                print(id,cx,cy)
                if(id==8):
                    cv2.circle(img,(cx,cy),15,(127,0,255),cv2.FILLED)
            mpdraw.draw_landmarks(img,handlmrk,mpHand.HAND_CONNECTIONS)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,2,(255,0,126),5)
    cv2.imshow("Image",img)

    cv2.waitKey(1)