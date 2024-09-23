import json
import random
def update_json_field(field, new_value, filename="data.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        data[field] = new_value
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        
        print(f"Đã cập nhật {field} với giá trị {new_value} trong {filename}")
    
    except FileNotFoundError:
        print(f"File {filename} không tồn tại.")
    except KeyError:
        print(f"Trường {field} không tồn tại trong dữ liệu.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")



with open("config/data.json") as f:
    settings = json.load(f)
    score = settings["user_score"]
    succes = settings["user_succes"]
    fail = settings["user_fail"]
    username = settings["user"]

if username != None:
    print(f"bạn có muốn tiếp tục với tài khoản trước đó không")
    k = input("Có (Y) / Không (N)")
    if k == "Y":
        print("chơi nhé")
    elif k == "N":
        user = input(" nhập tài khoản mới bạn muốn đăng nhập ")
        update_json_field("user", user, "config/data.json")
else:
    print("chưa đăng nhập ")
    user = input("nhập tên bạn muốn đăng nhập: ")
    update_json_field("user", user, "config/data.json")