from flask import Flask, request, jsonify, send_from_directory
import json, os
import flask_socketio
app = Flask(__name__)

def check_user_passw(thamso, pasw):
    with open("database/user-data.json") as f:
        settings = json.load(f)
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
        return jsonify({'error': 'Invalid request data'}), 400
    passs = data.get('pass')
    users = data.get('user')
    new_data = {
        f"{users}": {
            "password": f"{passs}" 
        }
    }
    oops = {
        f"{users}": {
            "user_score": 0,
            "user_correct": 0,
            "user_fail": 0,
            "rank": ""
        }
    }
    filepath = "database/user-data.json"
    filepath2 = "database/leaderboard.json"
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)
    with open(filepath2, 'w', encoding='utf-8') as file:
        json.dump(oops, file, ensure_ascii=False, indent=4)
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
# 127.0.0.1/download/info/{file} Lấy thông tin về file có trong foler không
# --- info.txt 
# ---- Lấy path file rồi gửi lại cho client

## chx test
@app.route('/download/<file_name>', methods=['GET'])
def download_baigiang(file_name):
    folder_name = file_name.rsplit('.', 1)[0]
    folder_path = os.path.join(baigiang, folder_name)
    
    return send_from_directory(folder_path, file_name)

###############################################


@app.route("/scores", methods=['POST'])
def submit_scores():
    name = request.json.get('name')
    correct = request.json.get('correct')
    score = request.json.get('score')
    wrong = request.json.get('wrong')
    if not name or correct is None or score is None or wrong is None:
        return ({"không có dữ liêu"}), 400
    with open("database/leadearboard.json") as f:
        data = json.load(f)
    data[name] = {"user_score": score, "user_correct": correct, "user_fail": wrong}
    return({"đã lưu thành công data"}), 200

import json

def sort():

    with open("database/leaderboard.json") as f:
        data = json.load(f)

    for student, scores in data.items():
        correct = scores.get("user_correct", 0)
        score = scores.get("user_score", 1) 
        if score == 0:  
            rate = 0
        else:
            rate = correct / score

        if rate >= 1.0:
            data[student]['rank'] = "Xuat Sac"
        elif rate >= 0.8:
            data[student]['rank'] = "Tot"
        elif rate >= 0.6:
            data[student]['rank'] = "Kha"
        else:
            data[student]['rank'] = "Trung Binh"

    with open("database/leaderboard.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    
    rank_priority = {
        "Xuat Sac": 0,
        "Tot": 1,
        "Kha": 2,
        "Trung Binh": 3
    }   

    sorted_data = sorted(data.items(), key=lambda x: (rank_priority.get(x[1]['rank'], 4), -x[1]['user_score']))
    

    filepath2 = "temp/turn.json"
    all_data = {}

    for student, student_data in sorted_data:
        all_data[student] = {
            "user_score": student_data["user_score"],
            "user_correct": student_data["user_correct"],
            "user_fail": student_data["user_fail"],
            "rank": student_data["rank"]
        }

   
    with open(filepath2, 'w', encoding='utf-8') as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

@app.route("/get_information_ranks", methods=['GET'])
def get_information_ranks():
    sort()
    with open("temp/turn.json") as f:
        data = json.load(f)
    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True)  
