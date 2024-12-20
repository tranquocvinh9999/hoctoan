import os
import sys

def resource_path(relative_path):
    """Lấy đường dẫn tuyệt đối tới tài nguyên, hoạt động cả khi đóng gói."""
    if getattr(sys, 'frozen', False):
            # If the app is frozen (compiled executable)
        base_path = os.path.dirname(sys.executable)
    else:
            # If running as a script (not frozen)
        base_path = "./"
    print(base_path)
    print(relative_path)
    return os.path.join(base_path, relative_path)


