from typing import List, Tuple
import cv2
import numpy as np

def find_squares(frame: np.ndarray) -> List[Tuple[int,int,int,int]]:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Размытие для удаления шума
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imshow("ee", blurred)

    edges = cv2.Canny(blurred, 50, 150)
    dilated = cv2.dilate(edges, np.ones((3,3), np.uint8), iterations=2)

    kernel = np.ones((25, 25), np.uint8)  # Размер ядра 5x5 (можно подобрать)
    closed_edges = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

    cv2.imshow("ff", closed_edges)
    contours, hierarchy = cv2.findContours(closed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cnt for cnt in contours if 10000 < cv2.contourArea(cnt) < 100000]
    squares = []
    for cnt in contours:
            
        epsilon = 0.1 * cv2.arcLength(cnt, True)  # 2% от длины контура
        approx = cv2.approxPolyDP(cnt, epsilon, True)  # Аппроксимация контура

        if len(approx) == 4:  # Если 4 угла, значит это прямоугольник
            squares.append(approx)
            
    return squares