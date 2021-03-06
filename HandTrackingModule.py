import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,maxhands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxhands=maxhands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(self.mode,self.maxhands,self.detectionCon,self.trackCon)
        self.mpdraw = mp.solutions.drawing_utils


    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handlmrk in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, handlmrk, self.mpHand.HAND_CONNECTIONS)

        return img
    def findPosition(self,img,handNo=0,draw=True):
        mylist=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                mylist.append([id,cx,cy])
                if draw :
                    cv2.circle(img, (cx, cy), 8, (127, 0, 255), cv2.FILLED)
        return mylist




def main():
    pTime, cTime = 0, 0
    cap = cv2.VideoCapture(0)

    detector=handDetector()

    while True:
        success, img = cap.read()
        img=detector.findHands(img)
        mylist=detector.findPosition(img,draw=False)
        if len(mylist)!=0:
            print(mylist[8])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 2, (255, 0, 126), 5)
        cv2.imshow("Image", img)

        cv2.waitKey(1)

if __name__=="__main__":
    main()
