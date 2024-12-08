from pymongo import MongoClient
import os
import json
from flask import Response
import gridfs

# Kết nối MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database']  # Đặt tên database
users_collection = db['users']
leaderboard_collection = db['leaderboard']
lectures_collection = db['lectures']
fs = gridfs.GridFS(db)  # Tạo GridFS

# Tạo thư mục nếu chưa tồn tại
baigiang = 'lectures'
if not os.path.exists(baigiang):
    os.makedirs(baigiang)

def check_user_passw(username, password):
    user = users_collection.find_one({"username": username})
    if not user:
        return False, False
    return True, user['password'] == password

def receive_new_user(username, password):
    if users_collection.find_one({"username": username}):
        return {'error': 'User already exists'}, 400

    new_user = {
        "username": username,
        "password": password
    }

    new_leaderboard = {
        "username": username,
        "user_score": 0,
        "user_correct": 0,
        "user_fail": 0,
        "rank": ""
    }

    users_collection.insert_one(new_user)
    leaderboard_collection.insert_one(new_leaderboard)
    return "ok", 200

def submit_scores(name, correct, score, wrong):
    if not name or correct is None or score is None or wrong is None:
        return "Missing data", 400

    rank = get_rank(correct, score)
    leaderboard_collection.update_one(
        {"username": name},
        {"$set": {"user_score": score, "user_correct": correct, "user_fail": wrong, "rank": rank}},
        upsert=True
    )
    return "Score updated successfully", 200

def get_scores(username=None):
    if username:
        user = leaderboard_collection.find_one({"username": username})
        if not user:
            return {'error': 'User not found'}, 404
        return user
    else:
        return list(leaderboard_collection.find())

def get_information_ranks():
    return list(leaderboard_collection.find().sort([("rank", 1), ("user_score", -1)]))

def reset_single_user(username):
    if not username:
        return {'error': 'No username provided'}, 400

    result = leaderboard_collection.update_one(
        {"username": username},
        {"$set": {"user_score": 0, "user_correct": 0, "user_fail": 0, "rank": ""}}
    )
    if result.matched_count == 0:
        return {'error': 'User not found'}, 404
    return "User data reset successfully", 200

def upload_baigiang(file, filename):
    """
    Lưu file lên MongoDB sử dụng GridFS
    """
    if not file:
        return {'error': 'No file uploaded'}, 400

    # Lưu file vào GridFS
    file_id = fs.put(file, filename=filename)

    # Lưu metadata (nếu cần)
    info = {
        "filename": filename,
        "file_id": file_id
    }
    lectures_collection.insert_one(info)

    return {'message': 'File uploaded successfully', 'file_id': str(file_id)}, 200

def download_baigiang(file_name):
    """
    Tải file từ MongoDB sử dụng GridFS
    """
    # Tìm file dựa trên tên
    file_data = fs.find_one({"filename": file_name})
    if not file_data:
        return {"error": "File not found."}, 404

    # Trả file dưới dạng response (dành cho Flask API)
    return Response(
        file_data.read(),
        mimetype="application/octet-stream",
        headers={"Content-Disposition": f"attachment;filename={file_name}"}
    )
def download_baigiang(file_name, folder_path):
    """
    Tải file từ MongoDB sử dụng GridFS và lưu vào thư mục chỉ định trên hệ thống.
    
    :param file_name: Tên file trong MongoDB.
    :param folder_path: Đường dẫn thư mục lưu file trên hệ thống.
    """
    # Kết nối tới MongoDB
    client = MongoClient('mongodb://localhost:27017/')  # Thay đổi thông tin kết nối nếu cần
    db = client['your_database_name']  # Thay 'your_database_name' bằng tên database của bạn
    fs = gridfs.GridFS(db)

    # Tìm file trong GridFS theo tên
    file_data = fs.find_one({"filename": file_name})
    if not file_data:
        print("File không tồn tại trong MongoDB.")
        return

    # Kiểm tra và tạo thư mục nếu chưa tồn tại
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Đường dẫn đầy đủ cho file
    output_path = os.path.join(folder_path, file_name)

    # Lưu file vào thư mục
    with open(output_path, 'wb') as f:
        f.write(file_data.read())
    print(f"File đã được tải xuống và lưu tại: {output_path}")

# Ví dụ gọi hàm
download_baigiang('bai_giang.pdf', './downloads')

def get_rank(correct, score):
    if score == 0:
        rate = 0
    else:
        rate = correct / score

    if rate >= 1.0:
        return "Xuat Sac"
    elif rate >= 0.8:
        return "Tot"
    elif rate >= 0.6:
        return "Kha"
    else:
        return "Trung Binh"

def sort_leaderboard():
    rank_priority = {
        "Xuat Sac": 0,
        "Tot": 1,
        "Kha": 2,
        "Trung Binh": 3
    }

    sorted_data = sorted(
        leaderboard_collection.find(),
        key=lambda x: (rank_priority.get(x['rank'], 4), -x['user_score'])
    )
    return sorted_data
