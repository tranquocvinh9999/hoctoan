import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Sử dụng API Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Tạo một Google Spreadsheet mới
spreadsheet = client.create("User Data")  # Tạo bảng tính mới với tên "User Data"
worksheet = spreadsheet.get_worksheet(0)  # Lấy sheet đầu tiên trong bảng tính

# Thiết lập cột đầu tiên
worksheet.append_row(["username", "password", "user_score", "user_correct", "user_fail", "rank"])  # Thêm tiêu đề cột

print("Đã tạo Google Sheet và thiết lập các cột!")

def create_sheet_if_not_exists(sheet_name):
    try:
        # Kiểm tra nếu bảng tính đã tồn tại
        spreadsheet = client.open(sheet_name)
        print(f"Spreadsheet '{sheet_name}' đã tồn tại.")
    except gspread.exceptions.SpreadsheetNotFound:
        # Tạo mới nếu bảng tính không tồn tại
        spreadsheet = client.create(sheet_name)
        worksheet = spreadsheet.get_worksheet(0)
        worksheet.append_row(["username", "password", "user_score", "user_correct", "user_fail", "rank"])
        print(f"Đã tạo bảng tính '{sheet_name}' mới.")

create_sheet_if_not_exists("User Data")
