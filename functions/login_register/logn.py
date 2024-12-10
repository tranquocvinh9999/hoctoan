import json
import requests
from functions.keyboard.keyboards import speak
from functions.microphone.micro import recognize_speech, check
from functions.resource_path.path import resource_path
# Function to update JSON file
def update_json(field, new_value, filename=None):
    try:
        with open(resource_path(filename), 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        data[field] = new_value
        with open(resource_path(filename), 'w', encoding='utf-8') as json_file:
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

