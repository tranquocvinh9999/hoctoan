from functions.login_register.logn import login_register_main
from functions.microphone.micro import check
from functions.keyboard.keyboards import speak
from AI.bot import generate_questions_from_a_name_AI
from AI.bot import get_data_from_given_question_AI
def menu():
    speak("hãy nói chương mà bạn muốn")
    k = check()
    t = k.lower()
    get_data_from_given_question_AI(t)

if __name__ == "__main__":
    menu()
