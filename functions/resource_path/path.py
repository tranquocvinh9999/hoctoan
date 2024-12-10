import os
import sys

def resource_path(relative_path):
    """Lấy đường dẫn tuyệt đối tới tài nguyên, hoạt động cả khi đóng gói."""
    try:
        # Khi chạy dưới dạng tệp .exe, PyInstaller trích xuất tệp vào _MEIxxx
        base_path = sys._MEIPASS
    except AttributeError:
        # Khi chạy trong môi trường phát triển
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
