from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
import gridfs


load_dotenv()

# Kết nối MongoDB, database connection
client = MongoClient(f"{os.getenv('DATABASE_URL')}", tls=True)
db = client["test_database"]
users_collection = db['users']
leaderboard_collection = db['leaderboard']
lectures_collection = db['lectures']
current_exercise_collection = db['current_exercise']
questions_collection = db['questions']

# Tạo thư mục nếu chưa tồn tại
baigiang = 'lectures'
if not os.path.exists(baigiang):
    os.makedirs(baigiang)

def check_user_passw(username, password):
    user = users_collection.find_one({"username": username})
    if not user:
        return False
    return True and user['password'] == password

def create_new_user(username, password):
    if users_collection.find_one({"username": username}):
        return False

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

    new_current_exercise = {
        "username" : username,
        "question": "",
        "correct": 0,
        "wrong": 0,
        "current": 0,
        "chapter": ""
    }

    users_collection.insert_one(new_user)
    leaderboard_collection.insert_one(new_leaderboard)
    current_exercise_collection.insert_one(new_current_exercise)

    return True

def update_current_exercise_by_username(username, question, correct, wrong, current, chapter):
    if not username or not question or correct is None or wrong is None or current is None or not chapter:
        return 300

    current_exercise_collection.update_one(
        {"username" : username},
        {"$set":{
            "question" : question,
            "correct" : correct,
            "wrong" : wrong,
            "current" : current,
            "chapter" : chapter,
    }})

    return 200

def get_current_exercise_by_username(username):
    if not username:
        return "Invalid username"

    return current_exercise_collection.find_one({"username":username})

def reset_current_exercise_by_username(username):
    current_exercise_collection.update_one(
        {"username" : username},
        {"$set":{ 
            "question": "",
            "correct": 0,
            "wrong": 0,
            "current": 0,
            "chapter": ""
 
    }})
    return 200

def remove_current_exercise_by_username(username):
    current_exercise_collection.delete_one({"username": username})
    return 200

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

def reset_all_user():
    leaderboard_collection.update_many({},
        {"$set": {"user_score": 0, "user_correct": 0, "user_fail": 0, "rank": ""}}
    )
    return "Reset all data successfully", 200

def insert_new_lecture(name, content):
    lectures_collection.insert_one({"name": name, "content": content})

def find_lecture_by_name(name):
    return lectures_collection.find_one({"name": name})

def find_all_lecture():
    return lectures_collection.find()

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

    if len(list(leaderboard_collection.find())) == 0:
        return []

    sorted_data = sorted(
        list(leaderboard_collection.find()),
        key=lambda x: (rank_priority.get(x['rank'], 4), -x['user_score'])
    )
    return sorted_data

def get_all_questions_by_chapter(chapter):
    return questions_collection.find_all({"chapter" : chapter})

def insert_new_question(chapter, question, answer):
    if not chapter or not question or not answer:
        return 300
    questions_collection.insert_one({
        "chapter" : chapter,
        "question" : question,
        "answer" : answer,
    })

    return 200

def get_all_chapter():
    return questions_collection.distinct("chapter")