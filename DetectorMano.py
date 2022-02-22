import cv2
import time
import numpy as np
import mediapipe as mp

class handetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        
        
        self.mphands= mp.solutions.hands
        self.hands=self.mphands.Hands(self.mode,self.maxHands
                                      ,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]


    def findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
    
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks: 
                if draw:              
                    self.mpDraw.draw_landmarks(img,handLms,self.mphands.HAND_CONNECTIONS)
            
        return img
    def findposition(self,img, handNo=0,draw=True ):
        self.lmList =[]
        
        if self.results.multi_hand_landmarks:  
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                    h,w,c=img.shape
                    cx,cy=int(lm.x*w), int(lm.y*h)
                    #print(id,cx,cy)
                    self.lmList.append([id, cx,cy])
                    if draw:
                        if id==10: #Para elegir el punto de la mano
                            cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)
        return self.lmList
    
    def findpositionV1(self,img, handNo=0,draw=True ):
        self.lmList =[]
        xList=[]
        yList=[]
        caja=[]
        if self.results.multi_hand_landmarks:  
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                    h,w,c=img.shape
                    cx,cy=int(lm.x*w), int(lm.y*h)
                    xList.append(cx)
                    yList.append(cy)
                    
                    self.lmList.append([id, cx,cy])
                    if draw:
                        if id==10: #Para elegir el punto de la mano
                            cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)
                            
            xmin,xmax=min(xList), max(xList)
            ymin,ymax=min(yList), max (yList)
            caja= xmin,ymin,xmax,ymax
            
            if draw:
                cv2.rectangle(img,(caja[0],caja[1]),(caja[2],caja[3]),(0,255,0),2)
        return self.lmList,caja
    
    def findfinger(self, img, rpoints, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for id, landm in enumerate(hand_landmarks.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(landm.x * w), int(landm.y * h)
                    if hand_landmarks != 0:
                        if id == 8:
                            rpoints[0].append((cx, cy))
        #if results.multi_hand_landmarks:
        #    for handLms in results.multi_hand_landmarks:
        #        cx = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width
        #        cy = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
        #        rpoints[0].append((cx, cy))

        #img = self.paint(img, rpoints)
        return rpoints
    
    def fingersUp(self):
        fingers = []
        # dedo gordo
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # resto de dedos
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    

    def paint(self, frame, rpoints):
        points = [rpoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], (100, 0, 255), 2)
        return frame
    