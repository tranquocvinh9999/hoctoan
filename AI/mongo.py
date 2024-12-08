from pymongo import MongoClient

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users_collection = db["users"]
leaderboard_collection = db["leaderboard"]

# Hàm kiểm tra username và password
def check_user_passw(username, password):
    user = users_collection.find_one({"username": username})
    if not user:
        return False, False
    if user["password"] == password:
        return True, True
    return True, False

# Hàm thêm người dùng mới
def add_new_user(username, password):
    if users_collection.find_one({"username": username}):
        return {"error": "User đã tồn tại"}
    
    users_collection.insert_one({"username": username, "password": password})
    leaderboard_collection.insert_one({
        "username": username,
        "user_score": 0,
        "user_correct": 0,
        "user_fail": 0,
        "rank": ""
    })
    return {"message": "Thêm user thành công"}

# Hàm tính rank
def get_rank(correct, score):
    if score == 0:
        return "Trung Binh"
    rate = correct / score
    if rate >= 1.0:
        return "Xuat Sac"
    elif rate >= 0.8:
        return "Tot"
    elif rate >= 0.6:
        return "Kha"
    else:
        return "Trung Binh"

# Hàm cập nhật điểm và xếp hạng
def submit_scores(username, correct, score, wrong):
    rank = get_rank(correct, score)
    leaderboard_collection.update_one(
        {"username": username},
        {"$set": {
            "user_score": score,
            "user_correct": correct,
            "user_fail": wrong,
            "rank": rank
        }}
    )
    return {"message": "Cập nhật điểm thành công"}

# Hàm lấy thông tin leaderboard
def get_leaderboard():
    data = list(leaderboard_collection.find({}, {"_id": 0}))
    rank_priority = {"Xuat Sac": 0, "Tot": 1, "Kha": 2, "Trung Binh": 3}
    sorted_data = sorted(data, key=lambda x: (rank_priority[x['rank']], -x['user_score']))
    return sorted_data

# Hàm reset thông tin một user
def reset_single_user(username):
    leaderboard_collection.update_one(
        {"username": username},
        {"$set": {
            "user_score": 0,
            "user_correct": 0,
            "user_fail": 0,
            "rank": ""
        }}
    )
    return {"message": "Reset thành công"}

# Ví dụ sử dụng
if __name__ == "__main__":
    # Thêm user mới
    print(add_new_user("user1", "password123"))

    # Kiểm tra username và password
    print(check_user_passw("user1", "password123"))

    # Cập nhật điểm
    print(submit_scores("user1", 8, 10, 2))

    # Lấy danh sách leaderboard
    print(get_leaderboard())

    # Reset thông tin user
    print(reset_single_user("user1"))
