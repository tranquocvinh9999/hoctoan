import json

# Đọc dữ liệu từ file JSON
with open("api/database/leadearboard.json") as f:
    data = json.load(f)
    
    # Tính toán hạng cho từng sinh viên
    for student, scores in data.items():
        correct = scores.get("user_correct", 0)
        score = scores.get("user_score", 1)  # Thay đổi giá trị mặc định nếu cần
        if score == 0:  # Kiểm tra trường hợp score bằng 0 để tránh chia cho 0
            rate = 0
        else:
            rate = correct / score
        
        if rate >= 1.0:
            data[student]['rank'] = "Xuất sắc"
        elif rate >= 0.8:
            data[student]['rank'] = "Tốt"
        elif rate >= 0.6:
            data[student]['rank'] = "Khá"
        else:
            data[student]['rank'] = "Trung Bình"
    
    # Sắp xếp dữ liệu theo điểm
    sorted_data = sorted(data.items(), key=lambda x: x[1]['user_score'], reverse=True)

# In ra danh sách đã sắp xếp
for student, scores in sorted_data:
    print(f"{student}: {scores['user_score']} điểm, Hạng: {scores['rank']}")

# Ghi dữ liệu đã cập nhật trở lại file JSON (nếu cần)
with open("api/database/leadearboard.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
