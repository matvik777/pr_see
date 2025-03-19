import cv2
import numpy as np
import matplotlib.pyplot as plt

# Загрузка изображения
image_path = "images/best_frame4.png"
image = cv2.imread(image_path)

# Преобразование в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('re2', gray)
# Размытие для удаления шума
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
cv2.imshow('re3', blurred)

edges = cv2.Canny(blurred, 50, 150)
dilated = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=2)

kernel = np.ones((25, 25), np.uint8)  # Размер ядра 5x5 (можно подобрать)
closed_edges = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

cv2.imshow('res4', closed_edges)
contours, hierarchy = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
filtered_contours = [cnt for cnt in contours if 10000 < cv2.contourArea(cnt) < 100000]
for cnt in filtered_contours:
    epsilon = 0.05 * cv2.arcLength(cnt, True)  # 2% от длины контура
    approx = cv2.approxPolyDP(cnt, epsilon, True)  # Аппроксимация контура

    if len(approx) == 4:  # Если 4 угла, значит это прямоугольник
        cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)
     

#cv2.drawContours(image, filtered_contours, -1, (0, 255, 0), 2)
cv2.imshow('re1', image)

cv2.waitKey(0)