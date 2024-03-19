import cv2
import time
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
detector = htm.handDetector()

prevTime = 0
currTime = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw = False)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList) != 0:
        print(lmList[8])

    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)