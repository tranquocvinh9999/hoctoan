import json
import random
from functions.keyboard.keyboards import speak
from functions.keyboard.keyboards import input_with_speak
from functions.microphone.micro import recognize_speech
from functions.microphone.micro import check
from main import mainop
#update(key, value, file dicts)
def update_json(field, new_value, filename="data.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        data[field] = new_value
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        
        print()
    except FileNotFoundError:
        print()
    except KeyError:
        print()
    except Exception as e:
        print()



with open("config/score.json") as f:
    settings = json.load(f)
    score = settings["user_score"]
    succes = settings["user_succes"]
    fail = settings["user_fail"]
    username = settings["user"]
with open("config/private.json") as f:
    settings = json.load(f)
    username = settings["username"]
    passwords = settings["password"]
def regis():
    speak("bạn chưa đăng kí tài khoản nào hãy đăng kí hãy nhập từ bàn phím")
    speak("lưu ý tên đăng nhập không có chữ in hoa và kí tự đặc biệt")
    user = input_with_speak("Nhập tên")
    passsword = input_with_speak("Nhập mật khẩu")
    if user.lower():
        update_json("username", user, "config/private.json")
    elif passsword.lower():
        update_json("password", passsword, "config/private.json")
    else:
        speak("tài khoản hoặc mật khẩu của bạn có kí tự in hoa hoặc là kí tự đặc biệt")
import requests
def loginpage():
    if username != None and passwords != None:
        speak(f"hình như bạn đã đăng nhập với tài khoản {username} phải không")
        speak("nếu phải bạn hãy nói đúng ngược lại bạn hãy nói không")
        op = check()
        if op == "phải" or "hải" or "ải":
            login_check()
            def login_check():
                k = input_with_speak(f"vui lòng bạn nhập mật khẩu tài khoản {username}")
                if k == passwords:
                    mainop()
                else:
                    speak("hãy nhập lại")
                    login_check()
        elif op == "không" or "hông" or "ông":
            def recall():
                speak("Lưu  ý bạn đăng nhập tài khoản và mật khẩu không được có chữ in hoa và kí tự đặc biệt")
                user = input_with_speak("bạn hãy nhập tài khoản")
                passw = input_with_speak("bạn hãy nhập mật khẩu")
                vai = 0
                dao = 0
                if user != None:
                    r = requests.post(f"127.0.0.1/check_user/?user={user}")
                    text = r.json().get('response')
                    if text == "tài khoản đúng":
                        vai = 1
                elif passw != None:
                    r = requests.post(f"127.0.0.1/check_passw/?pass={passw}&user={user}")
                    text = r.json().get('response')
                    if text == "mật khẩu đúng":
                        dao = 1
                if vai == 1 and dao == 1:
                    speak("bạn đã đăng nhập thành công")
                    update_json("username", user, "config/private.json")
                    update_json("password", passw, "config/private.json")
                elif vai == 1 and dao == 0:
                    speak("bạn đăng nhập sai mật khẩu của tài khoản")
                    speak("vui lòng đăng nhập lại tài khoản và mật khẩu")
                    recall()
                else:
                    speak("có vẻ cả tài khoản và mật khẩu đều sai")          
                    speak("hãy đăng nhập lại nhé")
                    recall()      
def login_register():
    if username == None and passwords == None:
        speak("Bạn muốn đăng nhập hay đăng kí")
        speak("nói đăng nhập để vào trang đăng nhập nói đăng ký để vào trang đăng ký")
        kt = check()
        if kt == "đăng nhập" or "nhập":
            loginpage()
        elif kt == "đăng ký" or "ký":
            regis()