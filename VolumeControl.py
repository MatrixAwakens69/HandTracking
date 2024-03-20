import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

widthCam, heightCam = 1280, 720
prevTime = 0
volBar = 600
volPercent = 0

detector = htm.handDetector(detectionCon=0.8)

cap = cv2.VideoCapture(0)
cap.set(3, widthCam)
cap.set(4, heightCam)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)

minVolume = volumeRange[0]
maxVolume = volumeRange[1]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime

    if len(lmList) > 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        # print(lmList[8], lmList[4])

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2-x1, y2-y1)

        vol = np.interp(length, [50,350], [minVolume, maxVolume])
        volBar = np.interp(length, [50, 350], [600, 150])
        volPercent = np.interp(length, [50, 350], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        if length > 350:
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)

    cv2.rectangle(img, (40, 150), (80, 600), (0, 255, 0), 3)
    cv2.rectangle(img, (40, int(volBar)), (80, 600), (0, 255, 0), cv2.FILLED)

    cv2.putText(img, f'Volume: {int(volPercent)} %', (40, 650), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.putText(img, f'FPS: {int(fps)}', (30, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)