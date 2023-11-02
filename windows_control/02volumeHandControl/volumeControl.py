import cv2
import time
import handTrackModule as htm
import volumeControlModule as vcm


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam) # to set window width and height
cap.set(4, hCam)

CTime = 0
pTime= 0

detector = htm.HandDetector(detectionCon=0.7)
volume_control = vcm.VolumeControl()

while True:
    success, img = cap.read()

    img = detector.findHands(img=img)
    lmList = detector.findPosition(img=img, draw=False)
    if len(lmList)!=0:
        length = volume_control.id_distance(img=img, lmList=lmList, id1=4, id2=8)
        volume_control.set_volume(length=length)
        volume_control.draw_volume_bar(img=img, length=length, ptr1_x=50, ptr1_y=150, ptr2_x=85, ptr2_y=400)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'fps: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)