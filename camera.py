import cv2


cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    cv2.imshow("result", img[0:200, 0:300])
    
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break