import cv2
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeControl:
    def __init__(self):

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)

        volume_range = self.volume.GetVolumeRange()
        self.min_vol = volume_range[0]
        self.max_vol = volume_range[1]

        self.vol_bar=400
        self.vol_per = 0
    
    def id_distance(self, img, lmList, id1, id2, drawLine=True):
        x1, y1 = lmList[id1][1], lmList[id1][2] # position of thumb tip
        x2, y2 = lmList[id2][1], lmList[id2][2] #position of index tip
        cx, cy = int((x1+x2)/2), int((y1+y2)/2) #centre of their pos
        length = math.hypot(x2-x1, y2-y1)

        if drawLine:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            if length<50:
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
        
        return math.hypot(x2-x1, y2-y1) # eucildian distance from centre
    
    def set_volume(self, length=0):
        vol = np.interp(length, [50, 300], [self.min_vol, self.max_vol])
        self.volume.SetMasterVolumeLevel(vol, None)

    def draw_volume_bar(self, img, length, ptr1_x, ptr1_y, ptr2_x, ptr2_y):

        self.vol_bar = np.interp(length, [50, 300], [ptr2_y, ptr1_y])
        self.vol_per = np.interp(length, [50, 300], [0, 100])

        cv2.rectangle(img, (ptr1_x, ptr1_y), (ptr2_x, ptr2_y), (255, 0, 0), 3)
        cv2.rectangle(img, (ptr1_x, int(self.vol_bar)), (ptr2_x, ptr2_y), (255, 0, 0), cv2.FILLED)

        cv2.putText(img, f'{int(self.vol_per)} %', (ptr1_x-10, ptr2_y+30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)