from flask import Flask, request, jsonify
import json
app = Flask(__name__)
def check_users(thamso):
    with open("database/user-data.json") as f:
        settings = json.load(f)
        if thamso in settings:
            return True
        else:
            return False
def check_passw(thamso, passs):
    with open("database/user-data.json") as f:
        settings = json.load(f)
        if thamso in settings:
            passw = settings[thamso]["password"]
            if passs == passw:
                return True
            else:
                return False

@app.route('/check_user', methods=['POST'])
def check_user():
    data = request.get_json()
    user = data.get('user')

    if check_users(user) == True:
        response = "tài khoản đúng"
    else:
        response = "tài khoản sai"
    return jsonify({'response': response})

@app.route('/check_passw', methods=['POST'])
def check_user():
    data = request.get_json()
    passs = data.get('pass')
    users = data.get('user')
    if check_users(users, passs) == True:
        response = "mật khẩu đúng"
    else:
        response = "mật khẩu sai"
    return jsonify({'response': response})
if __name__ == '__main__':
    app.run(debug=True)
