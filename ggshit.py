import gspread

# Truy cập Google Sheets thông qua URL
gc = gspread.service_account()  # Sử dụng tài khoản dịch vụ nếu cần, nếu không thì bỏ
spreadsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1iyyJsk61Zj6BJIGy9vKnrvq-SEA6BGv2dHM9lHwNrP8/edit")
worksheet = spreadsheet.sheet1  # Sheet đầu tiên trong bảng tính

# Hàm kiểm tra tên đăng nhập và mật khẩu
def check_user_passw(thamso, pasw):
    try:
        records = worksheet.get_all_records()  # Lấy tất cả dữ liệu từ bảng tính
        for record in records:
            if record["username"] == thamso:
                if record["password"] == pasw:
                    return True, True
                else:
                    return True, False
        return False, False
    except Exception as e:
        print(f"Error: {e}")
        return False, False

# Thêm người dùng mới
def add_new_user(user, passw):
    records = worksheet.get_all_records()
    for record in records:
        if record["username"] == user:
            return "Tài khoản đã tồn tại"
    
    # Thêm tài khoản mới vào Google Sheets
    worksheet.append_row([user, passw, 0, 0, 0, "Trung Binh"])  # Thêm username, password, và điểm
    return "Tạo tài khoản thành công"

# Cập nhật điểm và xếp hạng người dùng
def submit_scores(name, correct, score, wrong):
    records = worksheet.get_all_records()
    for i, record in enumerate(records):
        if record["username"] == name:
            rank = get_rank(correct, score)
            worksheet.update_cell(i + 2, 3, score)  # Cập nhật điểm
            worksheet.update_cell(i + 2, 4, correct)  # Cập nhật số câu đúng
            worksheet.update_cell(i + 2, 5, wrong)  # Cập nhật số câu sai
            worksheet.update_cell(i + 2, 6, rank)  # Cập nhật xếp hạng
            return "Cập nhật điểm thành công"
    return "Người dùng không tồn tại"

# Hàm tính toán xếp hạng
def get_rank(correct, score):
    rate = correct / score if score != 0 else 0
    if rate >= 1.0:
        return "Xuat Sac"
    elif rate >= 0.8:
        return "Tot"
    elif rate >= 0.6:
        return "Kha"
    else:
        return "Trung Binh"

# Lấy thông tin điểm số của người dùng
def get_scores(username=None):
    records = worksheet.get_all_records()
    if username is None:
        return records
    for record in records:
        if record["username"] == username:
            return record
    return "Người dùng không tồn tại"

# Reset dữ liệu của một người dùng
def reset_single_user(username):
    records = worksheet.get_all_records()
    for i, record in enumerate(records):
        if record["username"] == username:
            worksheet.update_cell(i + 2, 3, 0)  # Reset điểm
            worksheet.update_cell(i + 2, 4, 0)  # Reset số câu đúng
            worksheet.update_cell(i + 2, 5, 0)  # Reset số câu sai
            worksheet.update_cell(i + 2, 6, "Trung Binh")  # Reset xếp hạng
            return "Đã reset dữ liệu người dùng"
    return "Người dùng không tồn tại"

# Reset tất cả dữ liệu
def reset_all_data():
    records = worksheet.get_all_records()
    for i, record in enumerate(records):
        worksheet.update_cell(i + 2, 3, 0)  # Reset điểm
        worksheet.update_cell(i + 2, 4, 0)  # Reset số câu đúng
        worksheet.update_cell(i + 2, 5, 0)  # Reset số câu sai
        worksheet.update_cell(i + 2, 6, "Trung Binh")  # Reset xếp hạng
    return "Đã reset toàn bộ dữ liệu"

# Example usage
if __name__ == "__main__":
    # Thêm tài khoản mới
    print(add_new_user("new_user", "password123"))
    
    # Kiểm tra người dùng và mật khẩu
    valid_user, correct_pass = check_user_passw("new_user", "password123")
    print(f"User valid: {valid_user}, Password correct: {correct_pass}")
    
    # Cập nhật điểm số
    print(submit_scores("new_user", 10, 15, 5))
    
    # Lấy điểm của người dùng
    print(get_scores("new_user"))
    
    # Reset dữ liệu một người dùng
    print(reset_single_user("new_user"))
    
    # Reset toàn bộ dữ liệu
    print(reset_all_data())
