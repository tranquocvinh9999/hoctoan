import json
import requests
from functions.keyboard.keyboards import speak, nhap_va_noi
from functions.microphone.micro import recognize_speech, check

# Function to update JSON file
def update_json(field, new_value, filename=None):
    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        data[field] = new_value
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        print("File not found.")
    except KeyError:
        print("Key not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
with open("ip_host.json") as f:
    settings = json.load(f)
    ip = settings["ip"]
    port = settings["port"]


def req(users, pasw):
    data = {
       "user": users,
       "pass": pasw
    }
    res = requests.post(f"http://{ip}:{port}/check_user", json=data)
    valid_user = res.json().get("isCorrectUser")
    valid_passw = res.json().get("isCorrectPass")
    if valid_user == True and valid_passw == True:
        return True
    elif not valid_passw == False:
        return False
    return 2

def new_user(user, pasw):
    data = {
       "user": user,
       "pass": pasw
    }
    res = requests.post(f"http://{ip}:{port}/receive_new_user", json=data)

with open("config/score.json") as f:
    settings = json.load(f)
    score = settings["user_score"]
    succes = settings["user_correct"]
    fail = settings["user_fail"]
    username = settings["user"]

with open("config/private.json") as f:
    settings = json.load(f)
    usernames = settings["username"]
    passwords = settings["password"]


def regis():
    speak("Bạn chưa đăng kí tài khoản nào. Hãy đăng kí bằng cách nhập từ bàn phím.")
    speak("Lưu ý: Tên đăng nhập không có chữ in hoa và kí tự đặc biệt.")
    user = nhap_va_noi("Nhập tên")
    password = nhap_va_noi("Nhập mật khẩu")
    
    if user.islower() and user.isalnum():
        update_json("username", user)
    else:
        speak("Tên tài khoản có chữ in hoa hoặc kí tự đặc biệt.")
    
    if password.islower() and password.isalnum():
        update_json("password", password, "config/private.json")
        new_user(user, password, "config/private.json")
    else:
        speak("Mật khẩu có chữ in hoa hoặc kí tự đặc biệt.")
    
    speak("Hãy thoát phần mềm ra rồi đăng nhập lại.")


def loginpage():
    if username and passwords:
        speak(f"Hình như bạn đã đăng nhập với tài khoản {usernames}, phải không?")
        speak("Nếu phải, bạn hãy nói đúng, ngược lại hãy nói không.")
        op = check()
        if op in ["phải", "hải", "ải"]:
            login_check()
        elif op in ["không", "hông", "ông"]:
            recall()

def login_check():
    from main import mainop  
    k = nhap_va_noi(f"Vui lòng nhập mật khẩu tài khoản {usernames}.")
    if k == passwords:
        mainop()
    else:
        speak("Hãy nhập lại.")
        login_check()


def recall():
    speak("Lưu ý: Tài khoản và mật khẩu không được có chữ in hoa và kí tự đặc biệt.")
    user = nhap_va_noi("Bạn hãy nhập tài khoản.")
    passw = nhap_va_noi("Bạn hãy nhập mật khẩu.")

    if user and passw:
        if req(user, passw) == True:
            speak("Bạn đã đăng nhập thành công.")
            update_json("username", user, "config/private.json")
            update_json("password", passw, "config/private.json")
            update_json("user", user, "config/score.json")
        else:
            speak("Có vẻ cả tài khoản và mật khẩu đều sai.")
            speak("Hãy đăng nhập lại nhé.")
            recall()
    else:
        speak("Có vẻ đã có lỗi gì đó. Hãy đăng nhập lại.")
        recall()
isLogin = False
isRegis = False

def login_register_main():
    speak("Bạn muốn đăng nhập hay đăng kí?")
    speak("Nói 'đăng nhập' để vào trang đăng nhập, nói 'đăng ký' để vào trang đăng ký.")
    kt = check()
    if kt in ["đăng nhập", "nhập"]:
        loginpage()
    elif kt in ["đăng ký", "ký"]:
        regis()
