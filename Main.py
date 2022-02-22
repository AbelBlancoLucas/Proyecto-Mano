import cv2
import Mano1 as mano
import numpy as np
from cmath import cos
from math import sin


Wcam,Hcam= 0,0
cap=cv2.VideoCapture(0)
cap.set(3, Wcam)
cap.set(4, Hcam)

detector =mano.handetector(detectionCon=0.75)

altura=0
angulo=0
cambio=0
centrox=0
centroy=0
sel=0
fig=''
cambioAng=0


def seleccionador(img,lmList,fingers,ImgGuardado):
    global sel
    if fingers[1] and fingers[2] == False and fingers[0] and fingers[3] == False and fingers[4] and sel == 0:
        sel = 1
    if sel == 1:
        img=seleccionar_Imagen(img,lmList)
    if sel ==2:
        img,ImgGuardado=colocar_imagen(img,lmList,fingers,ImgGuardado)
    if sel==3:
        img,ImgGuardado=escalar_imagen(img,lmList,fingers,ImgGuardado)
    if sel==4:
        img,ImgGuardado=rotar_imagen(img,lmList,fingers,ImgGuardado)
    return img,ImgGuardado,

def seleccionar_Imagen(img,lmList):
    global sel
    global fig
    
    cv2.putText(img, 'Seleccionar Imagen', (500,20), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)
    
    cv2.rectangle(img,(0,0),(1280,150),(0,255,0),5)
    cv2.rectangle(img,(250,25),(350,125),(255,100,150),-1)
    cv2.circle(img,(550,75),50,(255,100,150),-1)
    Triangulo = np.array([[800, 25],[750, 125],[850, 125]], np.int32)
    cv2.fillPoly(img, [Triangulo], (255, 100, 150), cv2.LINE_AA)
    print("Iconos mode")
    if (pulgar_abajo(lmList)): 
        sel=0
    if ((lmList[8][2] > 25) and (lmList[8][2] < 125) and (lmList[8][1] < 350) and (lmList[8][1] > 250)):
        fig='cuad'
        sel=2
    if ((lmList[8][2] > 25) and (lmList[8][2] < 125) and (lmList[8][1] < 600) and (lmList[8][1] > 500)):
        fig='cir'
        sel=2
    if ((lmList[8][2] > 25) and (lmList[8][2] < 125) and (lmList[8][1] < 850) and (lmList[8][1] > 750)):
        fig='tri'
        sel=2
    return img

def colocar_imagen(img,lmList,fingers,ImgGuardado):
    global sel
    global altura
    global centrox
    global centroy
    global fig
    altura=640
    
    cv2.putText(img, 'Colocar Imagen', (500,20), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)
    
    if (pulgar_abajo(lmList)): 
        sel=0
    if fig == 'cuad':
        centrox=lmList[8][1]
        centroy=lmList[8][2]
        cv2.rectangle(img,(centrox-50,centroy-50),(centrox+50,centroy+50),(255,100,150),-1)
        if fingers[1] and fingers[2] and fingers[0] == False and fingers[3] == False and fingers[4] == False: 
            sel=3
        if fingers[1] and fingers[2] and fingers[0] and fingers[3]  and fingers[4] :
            sel=0
            cv2.rectangle(ImgGuardado,(centrox-50,centroy-50),(centrox+50,centroy+50),(255,100,150),-1)
    if fig == 'cir':
        centrox=lmList[8][1]
        centroy=lmList[8][2]
        img=cv2.circle(img,(centrox,centroy),50,(255,100,150),-1)
        if fingers[1] and fingers[2] and fingers[0] == False and fingers[3] == False and fingers[4] == False: 
            sel=3
        if fingers[1] and fingers[2] and fingers[0] and fingers[3]  and fingers[4] :
            sel=0
            cv2.circle(ImgGuardado,(centrox,centroy),50,(255,100,150),-1)
    if fig == 'tri':
        centrox=lmList[8][1]
        centroy=lmList[8][2]
        Triangulo = np.array([[centrox, centroy-50],[centrox-50, centroy+50],[centrox+50, centroy+50]], np.int32)
        cv2.fillPoly(img, [Triangulo], (255, 100, 150), cv2.LINE_AA)
        if fingers[1] and fingers[2] and fingers[0] == False and fingers[3] == False and fingers[4] == False: 
            sel=3
        if fingers[1] and fingers[2] and fingers[0] and fingers[3]  and fingers[4] : 
            sel=0
            Triangulo = np.array([[centrox, centroy-50],[centrox-50, centroy+50],[centrox+50, centroy+50]], np.int32)
            cv2.fillPoly(ImgGuardado, [Triangulo], (255, 100, 150), cv2.LINE_AA)
                
    return img,ImgGuardado

def escalar_imagen(img,lmList,fingers,ImgGuardado):
    global sel
    global altura
    global centrox
    global centroy
    global angulo
    global cambio
    global fig
    
    angulo=320
        
    cv2.putText(img, 'Escalar Imagen', (500,20), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.rectangle(img, (320, 30), (960,70), (0, 255, 0), 5) #BARRA
    cv2.rectangle(img, (altura, 30), (altura+10,70), (0, 255, 0), 5) #Selector
        
    if (pulgar_abajo(lmList)): 
        sel=0

    if fig == 'cuad':
        if ((lmList[8][1] < 960)and(lmList[8][1] > 320)and(lmList[8][2]<70)and(lmList[8][2]>30)):
            altura = lmList[8][1]
            cambio = altura - 640
        if (cambio < 0):
            cambio = round(cambio/7)

        cv2.rectangle(img,(centrox-cambio-50,centroy-cambio-50),(centrox+cambio+50,centroy+cambio+50),(255,100,150),-1)
            
        if fingers[1] and fingers[2] and fingers[0] == False and fingers[3]  and fingers[4] == False: 
            sel=4
        if fingers[1] and fingers[2] and fingers[0] and fingers[3]  and fingers[4] :
            sel=0
            cv2.rectangle(ImgGuardado,(centrox-cambio-50,centroy-cambio-50),(centrox+cambio+50,centroy+cambio+50),(255,100,150),-1)
            
    if fig == 'cir':
        if ((lmList[8][1] < 960)and(lmList[8][1] > 320)and(lmList[8][2]<70)and(lmList[8][2]>30)):
            altura = lmList[8][1]
        cambio = altura -640
        if (cambio < 0):
            cambio = round(cambio/7)
            
        cv2.circle(img,(centrox, centroy),50+cambio,(255,100,150),-1)
            
        if fingers[1] and fingers[2] and fingers[0] and fingers[3]  and fingers[4] :
            sel=0
            cv2.circle(ImgGuardado,(centrox, centroy),50+cambio,(255,100,150),-1)
            
    if fig == 'tri':
        if ((lmList[8][1] < 960)and(lmList[8][1] > 320)and(lmList[8][2]<70)and(lmList[8][2]>30)):
            altura = lmList[8][1]
        cambio = altura - 640
        if (cambio < 0):
            cambio = round(cambio/7)
        Triangulo = np.array([[centrox, centroy-50-cambio], [centrox-cambio-50, centroy+cambio+50], [centrox+cambio+50, centroy+cambio+50]], np.int32)
        cv2.fillPoly(img, [Triangulo], (255, 100, 150), cv2.LINE_AA)
            
        if fingers[1] and fingers[2] and fingers[0] == False and fingers[3] and fingers[4] == False: 
            sel=4
        if fingers[1] and fingers[2] and fingers[0] and fingers[3]  and fingers[4] : 
            sel=0
            Triangulo = np.array([[centrox, centroy-50-cambio], [centrox-cambio-50, centroy+cambio+50], [centrox+cambio+50, centroy+cambio+50]], np.int32)
            cv2.fillPoly(ImgGuardado, [Triangulo], (255, 100, 150), cv2.LINE_AA)
    
    return img,ImgGuardado

def rotar_imagen(img,lmList,fingers,ImgGuardado):
    global sel
    global altura
    global centrox
    global centroy
    global angulo
    global cambio
    global fig
    global cambioAng
       
    cv2.putText(img, 'Rotar Imagen', (500,20), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.rectangle(img, (320, 30), (960,70), (255, 0, 0), 5) #BARRA
    cv2.rectangle(img, (angulo, 30), (angulo+10,70), (255, 0, 0), 5) #Selector

    if (pulgar_abajo(lmList)): 
        sel=0

    if fig == 'cuad':
        if ((lmList[8][1] < 960)and(lmList[8][1] > 320)and(lmList[8][2]<70)and(lmList[8][2]>30)):
            angulo = lmList[8][1] 
        cambioAng = np.radians(round((angulo -320) / (640/360)))
                
        cuadrado = np.array([[calculoAngulosX(centrox-cambio-50, centroy-cambio-50, cambioAng,centrox,centroy),calculoAngulosY(centrox-cambio-50, centroy-cambio-50, cambioAng,centroy,centrox)],
                            [calculoAngulosX(centrox-cambio-50,centroy+cambio+50, cambioAng,centrox,centroy),calculoAngulosY(centrox-cambio-50, centroy+cambio+50, cambioAng,centroy,centrox)],
                            [calculoAngulosX(centrox+cambio+50,centroy+cambio+50, cambioAng,centrox,centroy),calculoAngulosY(centrox+cambio+50, centroy+cambio+50, cambioAng,centroy,centrox)],
                            [calculoAngulosX(centrox+cambio+50,centroy-cambio-50, cambioAng,centrox,centroy),calculoAngulosY(centrox+cambio+50, centroy-cambio-50, cambioAng,centroy,centrox)]],
                                np.int32)

        cv2.fillPoly(img, [cuadrado], (255, 100, 150), cv2.LINE_AA)
            
        if fingers[1] and fingers[2] and fingers[0] and fingers[3]  and fingers[4] :
            sel=0
            cuadrado = np.array([[calculoAngulosX(centrox-cambio-50, centroy-cambio-50, cambioAng,centrox,centroy),calculoAngulosY(centrox-cambio-50, centroy-cambio-50, cambioAng,centroy,centrox)],
                                 [calculoAngulosX(centrox-cambio-50,centroy+cambio+50, cambioAng,centrox,centroy),calculoAngulosY(centrox-cambio-50, centroy+cambio+50, cambioAng,centroy,centrox)],
                                 [calculoAngulosX(centrox+cambio+50,centroy+cambio+50, cambioAng,centrox,centroy),calculoAngulosY(centrox+cambio+50, centroy+cambio+50, cambioAng,centroy,centrox)],
                                 [calculoAngulosX(centrox+cambio+50,centroy-cambio-50, cambioAng,centrox,centroy),calculoAngulosY(centrox+cambio+50, centroy-cambio-50, cambioAng,centroy,centrox)]],
                                 np.int32)

            cv2.fillPoly(ImgGuardado, [cuadrado], (255, 100, 150), cv2.LINE_AA)
                
    if fig == 'tri':
        if ((lmList[8][1] < 960)and(lmList[8][1] > 320)and(lmList[8][2]<70)and(lmList[8][2]>30)):
            angulo = lmList[8][1] 
        cambioAng = np.radians(round((angulo -320) / (640/360)))
            
        Triangulo = np.array([[calculoAngulosX(centrox, centroy-50-cambio, cambioAng,centrox,centroy),calculoAngulosY(centrox, centroy-50-cambio, cambioAng,centroy,centrox)],
                                [calculoAngulosX(centrox-cambio-50,centroy+cambio+50, cambioAng,centrox,centroy),calculoAngulosY(centrox-cambio-50, centroy+cambio+50, cambioAng,centroy,centrox)],
                                [calculoAngulosX(centrox+cambio+50, centroy+cambio+50, cambioAng,centrox,centroy),calculoAngulosY(centrox+cambio+50, centroy+cambio+50, cambioAng,centroy,centrox)]]
                                ,np.int32)
        cv2.fillPoly(img, [Triangulo], (255, 100, 150), cv2.LINE_AA)

        if fingers[1] and fingers[2] and fingers[0] and fingers[3]  and fingers[4] : 
            sel=0
            Triangulo = np.array([[calculoAngulosX(centrox, centroy-50-cambio, cambioAng,centrox,centroy),calculoAngulosY(centrox, centroy-50-cambio, cambioAng,centroy,centrox)],
                                [calculoAngulosX(centrox-cambio-50,centroy+cambio+50, cambioAng,centrox,centroy),calculoAngulosY(centrox-cambio-50, centroy+cambio+50, cambioAng,centroy,centrox)],
                                [calculoAngulosX(centrox+cambio+50, centroy+cambio+50, cambioAng,centrox,centroy),calculoAngulosY(centrox+cambio+50, centroy+cambio+50, cambioAng,centroy,centrox)]]
                                , np.int32)
            cv2.fillPoly(ImgGuardado, [Triangulo], (255, 100, 150), cv2.LINE_AA)
    return img,ImgGuardado

def calculoAngulosX(x,y,angulo,centrox,centroy):
    res=(x-centrox)*cos(angulo)-(y-centroy)*sin(angulo)+centrox
    return round(res.real)

def calculoAngulosY(x,y,angulo,centroy,centrox):
    res=(x-centrox)*sin(angulo)+(y-centroy)*cos(angulo)+centroy
    return round(res.real)

def pulgar_abajo(lmList):
    bol=False
    if ((lmList[4][2] > lmList[8][2]) and (lmList[4][2] > lmList[12][2]) 
     and (lmList[4][2] > lmList[16][2]) and (lmList[4][2] > lmList[20][2]) and (lmList[4][2] > lmList[3][2]) and 
    (lmList[4][2] > lmList[5][2]) and (lmList[4][2] > lmList[17][2])): 
        bol=True
    return bol

def borrar_todo(img,imgGuardado,lmList):
    global sel
    if(sel==0):
        #colocoar una x arriba a la izq para borrar todo
        img = cv2.line(img,(1150,30),(1200,80),(0,0,255),5)
        img = cv2.line(img,(1200,30),(1150,80),(0,0,255),5)       
        if ((lmList[8][2] > 30) and (lmList[8][2] < 80) and (lmList[8][1] < 1200) and (lmList[8][1] > 1150)):
            imgGuardado = np.zeros((720, 1280, 3), np.uint8)
    return img,imgGuardado



def main():
    Wcam,Hcam= 1280, 720
    cap=cv2.VideoCapture(0)
    cap.set(3, Wcam)
    cap.set(4, Hcam)
    print(cap.get(3))
    print(cap.get(4))
    detector = mano.handetector(detectionCon=0.65,maxHands=1)
    xp, yp = 0, 0
    drawColor = (0, 233, 255)
    ImgGuardado = np.zeros((720, 1280, 3), np.uint8)
    global altura
    global angulo
    global cambio
    global centrox
    global centroy
    global sel
    global fig
    global cambioAng
    while True:
        
        _, img = cap.read()
        img = cv2.flip(img, 1)
        
        img = detector.findHands(img)
        lmList = detector.findposition(img, draw=False) 
        
        
        if len(lmList) != 0:
            
            x1, y1 = lmList[8][1:]

            fingers = detector.fingersUp()
            
            img,ImgGuardado=borrar_todo(img,ImgGuardado, lmList)
            
            img,ImgGuardado=seleccionador(img, lmList, fingers, ImgGuardado)

            if fingers[1] and fingers[2] == False and fingers[0] == False and fingers[3] == False and fingers[4] == False and sel==0 :
                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                cv2.line(ImgGuardado, (xp, yp), (x1, y1), drawColor, 15)
            xp, yp = x1, y1

        imgGray = cv2.cvtColor(ImgGuardado, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("1", imgGray)
        _, imgaux = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        #cv2.imshow("2", imgaux)
        imgaux = cv2.cvtColor(imgaux,cv2.COLOR_GRAY2BGR)
        #cv2.imshow("3", imgaux)
        img = cv2.bitwise_and(img,imgaux)#Hace una and y aquello que valga 0 en b lo pone a 0 tambien en a(dibuja en a en negro)
        #cv2.imshow("4", img)
        #cv2.imshow("5", ImgGuardado)
        img = cv2.bitwise_or(img,ImgGuardado)#Hace un or y suma donde estaba cero antes ('contorno') el color que habia en imgGuardado
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        
if __name__ == "__main__":
    main()