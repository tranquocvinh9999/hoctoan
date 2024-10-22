from flask import Flask, request, jsonify
import json

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

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

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
    
    filepath = "database/user-data.json"
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)
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
        # Khong can phai if tai vi da handle trong function check_user roi
        'isCorrectPass': correct_pass
    }
    
    return jsonify(response)
#######################################################################33

if __name__ == '__main__':
    app.run(debug=True)  
