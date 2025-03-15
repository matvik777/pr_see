import cv2


cap = cv2.VideoCapture("videos/video_1.mp4")
if not cap.isOpened():
    print("Error video not opeened")
    exit()
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  
print(f"{fps} \n {frame_count} \n {width} {height}")
best_frame = None
best_frame_number = None
best_sharpness = -1
while cap.isOpened():
    current_frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES) - 1)

    ret, frame = cap.read()
    if not ret:  # Если кадры закончились, выходим
        print("End of video")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #переводим в чб
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    sobel = sobelx**2 + sobely**2
    variance = sobel.var()
    
    # laplacian = cv2.Laplacian(gray, cv2.CV_64F) #лапласиан тоже дает 108 кадр
    # variance = laplacian.var()
    if variance> best_sharpness:
        best_sharpness = variance
        best_frame = frame.copy()
        best_frame_number = current_frame_number
    
    
    
    
    time_frame = int(1000/ fps)
    cv2.imshow("Видео", frame)
    key = cv2.waitKey(time_frame) & 0xFF  # Получаем нажатую клавишу
    if key == 27:  # Если нажата ESC (код 27)
        break  # Выходим из цикла
cv2.imwrite("images/best_frame.png", best_frame)
print(F"{best_frame_number}    {best_sharpness}")
cap.release()
cv2.destroyAllWindows()