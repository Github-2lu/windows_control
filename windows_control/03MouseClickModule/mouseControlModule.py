import cv2
import mouse
import time
import numpy as np

class MouseControl:
    def __init__(self, id1, id2):
        self.id1, self.id2 = id1, id2

        self.plocX=0
        self.plocY=0
        return

    def trackHand(self, img, lmList, frameR, wCam, hCam):
        self.x1, self.y1 = lmList[self.id1][1:]
        self.x2, self.y2 = lmList[self.id2][1:]

        cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255, 0, 255), 2)
        return

    def moveCursor(self, img, wCam, hCam, frameR, wscreen, hscreen, smoothening, draw=True):
        # convert coodinates to laptop resolution
        # frameR is needed as while moveing cursor down hand detection is not possible
        x3 = np.interp(self.x1, (frameR, wCam-frameR), (0, wscreen))
        y3 = np.interp(self.y1, (frameR, hCam-frameR), (0, hscreen))
        # values are smoothened so that it don't flickker
        clocX = self.plocX + (x3-self.plocX) / smoothening
        clocY = self.plocY + (y3-self.plocY) / smoothening

        # moving mouse
        # pyautogui can also be used but it drop fps of handtracking drasticly
        mouse.move(wscreen-clocX, clocY)
        if draw:
            cv2.circle(img, (self.x1, self.y1), 10, (0, 255, 0), cv2.FILLED)
        self.plocX, self.plocY = clocX, clocY
        return

    def click(self, img, length, lineinfo, draw=True):
        if length<50:
            if draw:
                cv2.circle(img, (lineinfo[4], lineinfo[5]), 10, (0, 255, 0), cv2.FILLED)
            #pag.click()
            mouse.click('left')
            time.sleep(0.3)
        return 