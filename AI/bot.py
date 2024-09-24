import random
from functions.keyboard.keyboards import speak
from AI.functions.math import nhan, cong, tru
# hello
def random_10_cau_hoi_nhan_cong_tru():
    questions = []
    dem = 0
    lists = ["nhan", "cong", "tru"]

    while dem < 10:
        k = random.choice(lists)
        
        if k == "nhan":
            a, b, res = nhan()
            questions.append((1, a, b, res))
        elif k == "cong":
            a, b, res = cong()
            questions.append((2, a, b, res))
        elif k == "tru":
            a, b, res = tru()
            questions.append((3, a, b, res))
        
        dem += 1

    return questions
