from flask import Flask, request, jsonify, send_from_directory
import json, os
import flask_socketio
import json
app = Flask(__name__)
# 123
def check_user_passw(thamso, pasw):
    with open("database/user-data.json") as f:
        settings = json.load(f)
        if thamso not in settings:
            return False, False
        if thamso in settings:
            passw = settings[thamso]["password"]
            if pasw == passw:
                return True, True 
            else:
                return True, False 
        else:
            return False, False  



@app.route('/receive_new_user', methods=['POST'])
def new():
    data = request.get_json()
    if not data or 'pass' not in data or 'user' not in data:
        return jsonify({'error': 'lỗi'}), 400
    
    passs = data.get('pass')
    users = data.get('user')
    with open("database/user-data.json") as f:
        settings = json.load(f)
    if users in settings:
        return jsonify({'error': 'đã có 1 tài khoản trước rồi'}), 400
    new_data = {
        users: {
            "password": passs 
        }
    }
    oops = {
        users: {
            "user_score": 0,
            "user_correct": 0,
            "user_fail": 0,
            "rank": ""
        }
    }
    
    filepath = "database/user-data.json"
    filepath2 = "database/leaderboard.json"
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}

    user_data.update(new_data)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(user_data, file, ensure_ascii=False, indent=4)
    
    try:
        with open(filepath2, 'r', encoding='utf-8') as file:
            leaderboard_data = json.load(file)
    except FileNotFoundError:
        leaderboard_data = {}

    leaderboard_data.update(oops)
    
    with open(filepath2, 'w', encoding='utf-8') as file:
        json.dump(leaderboard_data, file, ensure_ascii=False, indent=4)
    
    return "ok"


@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.get_json()
    if not data or 'pass' not in data or 'user' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    passs = data.get('pass')
    users = data.get('user')
    user_valid, correct_pass = check_user_passw(users, passs)
    response = {
        'isCorrectUser': user_valid,
        'isCorrectPass': correct_pass
    }
    
    return jsonify(response)
#######################################################################33
baigiang = 'lectures'


if not os.path.exists(baigiang):
    os.makedirs(baigiang)
def create_file(file_name):
    foldername = file_name.split('.')[0]
    folder_path = os.path.join(baigiang, foldername)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path
def get_rank(correct, score):
    rate: float
    rank: str
    if score == 0:  
        rate = 0
    else:
        rate = correct / score

    if rate >= 1.0:
        rank = "Xuat Sac"
    elif rate >= 0.8:
        rank = "Tot"
    elif rate >= 0.6:
        rank = "Kha"
    else:
        rank = "Trung Binh"
    return rank
    
def sort():
    filepath = "database/leaderboard.json"
    with open(filepath) as f:
        data = json.load(f)

    rank_priority = {
        "Xuat Sac": 0,
        "Tot": 1,
        "Kha": 2,
        "Trung Binh": 3
    }   

    sorted_data = sorted(data.items(), key=lambda x: (rank_priority.get(x[1]['rank'], 4), -x[1]['user_score']))

    all_data = {}
    print(sorted_data)
    for student, student_data in sorted_data:
        all_data[student] = {
            "user_score": student_data["user_score"],
            "user_correct": student_data["user_correct"],
            "user_fail": student_data["user_fail"],
            "rank": get_rank(student_data["user_correct"], student_data["user_score"])
        }

    print(all_data)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

@app.route('/upload', methods=['POST'])
def upload_baigiang():

    if 'file' not in request.files:
        return jsonify({'error': 'không có file nào được up lên'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'không có file'}), 400

    folder_path = create_file(file.filename)
    file_path = os.path.join(folder_path, file.filename)
    file.save(file_path)

    info_file = os.path.join(folder_path, 'info.txt')
    info = {
        "filename": {file.filename}
    }
    # data = []
    # data.append(info)
    # json.dump(data, "database/lectures.json", ensure_ascii=False, indent=4)

    with open(info_file, 'w', encoding='utf-8') as f:
        f.write(f"File: {file.filename}\n")
        f.write(f"Path: {file_path}\n")
    
    return jsonify({'message': 'Tải bài giảng thành công', 'folder': folder_path}), 200
# 127.0.0.1/download/{file}
# 127.0.0.1/download/info.txt/{file} Lấy thông tin về file có trong foler không
# --- info.txt 
# ---- Lấy path file rồi gửi lại cho client

## chx test
# /download/?user=asdfa

@app.route('/download/<file_name>', methods=['GET'])
def download_baigiang(file_name):
    folder_name = file_name.rsplit('.', 1)[0]  
    folder_path = os.path.join(baigiang, folder_name)
    

    file_path = os.path.join(folder_path, file_name)
    

    if os.path.exists(file_path):
        return send_from_directory(folder_path, file_name)
    else:

        return jsonify({"error": "File không tồn tại."}), 404  


@app.route("/scores", methods=['POST'])

def submit_scores():
    name = request.json.get('name')
    correct = request.json.get('correct')
    score = request.json.get('score')
    wrong = request.json.get('wrong')
    if not name or correct is None or score is None or wrong is None:
        return "không có dữ liêu"
    with open("database/leaderboard.json", "r") as f:
        data = json.load(f)
    data[name] = {"user_score": score, "user_correct": correct, "user_fail": wrong, "rank": get_rank(correct, score)}
    sort()
    with open("database/leaderboard.json", "w") as f:
        json.dump(data, f, indent=4)
    return  "đã lưu thành công data"

@app.get("/scores")
@app.get("/scores/<username>")
def get_scores(username):
    with open("database/leaderboard.json") as f:
        data = json.load(f)
    if username == None:
        return data
    if not data[username]:
        return jsonify({'error': 'Không có user'}), 400
    return data[username]

@app.route("/get_information_ranks", methods=['GET'])
def get_information_ranks():
    sort()
    with open("database/leaderboard.json") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/reset_single_user", methods=['POST'])
def reset_single_user():
    """Reset dữ liệu của một người dùng cụ thể."""
    username = request.json.get('username')
    if not username:
        return jsonify({'error': 'Không có username được cung cấp'}), 400
    
    filepath = "database/leaderboard.json"
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("hah")
        return jsonify({'error': 'Không tìm thấy file dữ liệu'}), 404

    if username not in data:
        return jsonify({'error': 'Người dùng không tồn tại'}), 404
    data[username] = {
        "user_score": 0,
        "user_correct": 0,
        "user_fail": 0,
        "rank": "Trung Binh"
    }

    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return jsonify({'message': f'Dữ liệu của {username} đã được reset thành công.'}), 200


@app.route("/reset_data_on_server", methods=['POST'])
def reset_data_on_server():
    """Reset toàn bộ dữ liệu trong leaderboard.json."""
    filepath = "database/leaderboard.json"
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("hah")
        return jsonify({'error': 'Không tìm thấy file dữ liệu'}), 404
    for username in data:
        data[username] = {
            "user_score": 0,
            "user_correct": 0,
            "user_fail": 0,
            "rank": "Trung Binh"
        }

    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return jsonify({'message': 'Dữ liệu trên server đã được reset thành công.'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)  
