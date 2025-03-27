import sys
import cv2
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout, QSlider, QScrollArea,
    QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Webcam") 
        self.resize(1300,900)
        
        
        self.label_info = QLabel("Информация о камере/кадре отобразится здесь.")
        
        self.label_video = QLabel("Video not faund")
        self.label_video.setMinimumSize(1280, 720)
       # Масштабировать изображение внутри QLabel

        self.label_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.label_video)
      
        self.scroll_area.setMinimumSize(1280, 720)  # Минимальный размер, который ты хочешь
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Позволяет растягиваться        
        self.label_zoom_value = QLabel("Zomm: 100%")
        
        self.slider_zoom = QSlider(Qt.Orientation.Horizontal)
        self.slider_zoom.setMinimum(10)
        self.slider_zoom.setMaximum(300)
        self.slider_zoom.setValue(100)
        self.slider_zoom.setTickInterval(10)
        self.slider_zoom.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_zoom.valueChanged.connect(self.on_zoom_changed)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.label_info)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.label_zoom_value)
        button_layout.addWidget(self.slider_zoom)
        
        main_layout = QVBoxLayout()
        
        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)
        main_layout.addWidget(self.scroll_area,  alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Новая ширина
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        if not self.cap.isOpened:
            self.label_info.setText("Не удалось открыть видео")
            return
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.scale_factor = 1.0
    
    def on_zoom_changed(self, value: int):
        
        self.scale_factor = value / 100.0
        self.label_zoom_value.setText(f"Zoom: {value}")
    
       
    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                
                gimg = QImage(
                    frame_rgb.data, w , h, bytes_per_line,
                    QImage.Format.Format_RGB888
                    
                )
                
                pixmap_original = QPixmap.fromImage(gimg)
                
                scaled_w = int(pixmap_original.width()* self.scale_factor)
                scaled_h = int(pixmap_original.height()* self.scale_factor)
                
                pixmap_scaled = pixmap_original.scaled(
                    scaled_w, scaled_h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.label_video.setPixmap(pixmap_scaled)
                self.label_video.resize(pixmap_scaled.size())
                self.label_info.setText(f"Кадр получен: {w}x{h}")
            else:
                self.label_info.setText("Error read frame")
        else:
            self.label_info.setText("Camera not openned")
            
    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        event.accept()
        
def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()