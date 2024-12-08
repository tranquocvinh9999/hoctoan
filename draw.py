import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPainter, QColor, QPen
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import easyocr

class DrawingBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: white;")
        
        # Initialize self.pen as QPen, not QPainter
        self.pen = QPen(Qt.black)  # Màu đen để vẽ
        self.drawing = False
        self.last_point = None
        self.paths = []
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.pen)  # Set the pen to a QPen object
        
        # Vẽ các đường đã vẽ
        for path in self.paths:
            painter.drawLine(path[0], path[1])

    def mousePressEvent(self, event):
        # Bắt đầu vẽ khi nhấn chuột
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        # Tiếp tục vẽ khi di chuyển chuột
        if self.drawing:
            current_point = event.pos()
            self.paths.append((self.last_point, current_point))  # Lưu điểm vẽ
            self.last_point = current_point
            self.update()

    def mouseReleaseEvent(self, event):
        # Kết thúc vẽ khi thả chuột
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def get_image(self):
        # Lấy hình ảnh từ phần bảng trắng
        image = self.grab(self.rect()).toImage()
        return image

    def clear(self):
        # Xóa toàn bộ bảng vẽ
        self.paths.clear()
        self.update()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bảng trắng học sinh")
        self.setGeometry(100, 100, 800, 600)

        # Tạo bảng vẽ
        self.drawing_board = DrawingBoard()

        # Nút nhận diện chữ
        self.capture_button = QPushButton("Nhận diện chữ", self)
        self.capture_button.clicked.connect(self.capture_image)

        # Nút xóa bảng vẽ
        self.clear_button = QPushButton("Xóa bảng vẽ", self)
        self.clear_button.clicked.connect(self.clear_drawing)

        # Ô hiển thị chữ đã nhận diện
        self.recognized_text_label = QLabel(self)

        # Layout cho giao diện
        layout = QVBoxLayout()
        layout.addWidget(self.drawing_board)
        layout.addWidget(self.capture_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.recognized_text_label)
        self.setLayout(layout)

        # Khởi tạo EasyOCR
        self.reader = easyocr.Reader(['en', 'vi'])  # Thêm các ngôn ngữ cần nhận diện

    def capture_image(self):
        # Chụp lại hình ảnh của bảng vẽ
        image = self.drawing_board.get_image()
        recognized_text = self.recognize_text_from_image(image)
        self.recognized_text_label.setText(recognized_text)

    def recognize_text_from_image(self, image):
        # Lưu ảnh bảng vẽ
        image.save("drawing.png")

        # Sử dụng EasyOCR để nhận diện chữ từ ảnh
        result = self.reader.readtext('drawing.png')

        # Trích xuất chữ đã nhận diện từ kết quả
        recognized_text = '\n'.join([text[1] for text in result])  # Kết hợp các dòng chữ
        return recognized_text

    def clear_drawing(self):
        # Xóa bảng vẽ
        self.drawing_board.clear()
        self.recognized_text_label.clear()


# Khởi tạo ứng dụng
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
