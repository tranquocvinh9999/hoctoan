import pymongo
from pymongo import MongoClient

client = MongoClient("")
database = client["db"]
leader = database['leader']
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
    
def submit_scores(name, correct, wrong, score):
    new_data = {
        "name": name,
        "user_score": score,
        "user_correct": correct,
        "user_fail": wrong,
        "rank": get_rank(correct, score)
    }
    leader.update_one(
        {"name": name},
        {"$set": new_data},
        upsert= True)
    return ({"bạn đã xong gửi dữ liệu lên máy chủ"}), True
