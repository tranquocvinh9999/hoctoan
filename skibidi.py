import tkinter as tk
import pyttsx3

# Khởi tạo công cụ phát âm thanh
engine = pyttsx3.init()

# Cấu hình công cụ phát âm thanh
engine.setProperty('rate', 150)  # Tốc độ phát âm
engine.setProperty('volume', 1)  # Âm lượng

# Chức năng phát âm thanh thông báo vẽ
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Chức năng vẽ lên canvas
def draw(event):
    x, y = event.x, event.y
    canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")  # Vẽ hình tròn nhỏ
    speak(f"Vẽ tại vị trí: {x}, {y}")

# Tạo giao diện người dùng
root = tk.Tk()
root.title("Bảng Vẽ Dành Cho Người Khiếm Thị")

# Tạo một canvas để vẽ
canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Thêm sự kiện khi người dùng nhấn chuột để vẽ
canvas.bind("<B1-Motion>", draw)

# Thông báo khi chương trình bắt đầu
speak("Chào bạn, vui lòng bắt đầu vẽ!")

# Chạy giao diện người dùng
root.mainloop()
