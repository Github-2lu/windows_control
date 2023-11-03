import cv2
import time
import handTrackModule as htm
import pyautogui as pag
import mouseControlModule as mcm

wCam = 640
hCam = 480
frameR = 100 # frame reduction for when cursor is going down
smoothening = 5

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

wscreen, hscreen = pag.size()
#print(wscreen, hscreen)

#################
#     steps
# 1. find hand landmarks
# 2. Get the tip of the index and middle finger
# 3. check which fingers are up
# 4. only index finger: moving mode
# 5. convert coordinates to laptop resolution
# 6. smoothen values so that mouse don't flickker
# 7. move mouse
# 8. Both index and middle fingers are up : clicking mode
# 9. find distance b/w index and middle fingers
# 10. click mouse if distance short
# 11. frame rate 
# 12. display
###################

pTime = 0
id1 = 8 # index finger top
id2 = 12 # middle finger top

detector = htm.HandDetector(maxHands=1)
mouseControl = mcm.MouseControl(id1, id2)



while True:
    #1. find handLandMarks
    _, img = cap.read()
    img = detector.findHands(img)
    lmList,_ = detector.findPosition(img)

    if len(lmList)!=0:
        mouseControl.trackHand(img=img, lmList=lmList, frameR=frameR, wCam=wCam, hCam=hCam)

        #print(x1, y1, x2, y2)
        # 2, 3 check which fingers are up
        # fingers list[thumb top, index top, middle top, ring top, pinky top]
        fingers = detector.fingersUp()
        # 4. only index finger moving mode
        if fingers[1]==1 and fingers[2]==0:
            mouseControl.moveCursor(img, wCam, hCam, frameR, wscreen, hscreen, smoothening)
        # both index and middle finger are up clicking mode
        if fingers[1]==1 and fingers[2]==1:
            # find distance b/w index and middle finger
            length, img, lineinfo = detector.findDistance(id1, id2, img)
            # click mouse if length is short
            mouseControl.click(img, length, lineinfo)

    # frame rate        
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f"fps:{int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
# display
    cv2.imshow("Image", img)
    cv2.waitKey(1)