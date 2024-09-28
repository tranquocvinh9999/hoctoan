import random
from functions.keyboard.keyboards import speak
from AI.functions.math import nhan, cong, tru
from functions.keyboard.keyboards import input_with_speak
import google.generativeai as genai
import os
import json
# 10 cau hoi
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
#ai đây
def generate_questions_from_a_name_AI(name):
    genai.configure(api_key="AIzaSyDZKaDnvhAfcNVUfKJiDoGb1bHYNGyAFeA")
    model = genai.GenerativeModel("gemini-1.5-flash")
    # response = model.generate_content(f"""giả sử bạn là một giáo viên dạy toán. Đây là bài toán tôi đưa ra: Hãy giải bài toán: x + 1 = 3. Kết quả học sinh gửi tôi là
    # x = 3. Bạn hay kiểm tra nếu kết quả này là đúng hay sai. Nếu đúng không tạo câu trả lời mà chỉ in ra đúng, sai thì trả về các bước để khắc phúc nhưng không được nêu ra đáp án""")
    response = model.generate_content(f"""Đây là chương của chủ đề của một bài trong sách toán sáu tên là {name} thuộc sách mới KẾT NỐI TRI THỨC 
của phòng giáo dục Việt Nam bạn hãy viết cho tôi 5 bài tập về bài đó giúp tôi để tôi cho các học sinh của tôi làm nữa lưu ý các bài tập có định dạng CÂU HỎI:CÂU TRẢ LỜI và lược bỏ các câu trả lời của bạn không cần thiết
bỏ các chữ in hoa khi bạn trả về text cho tôi nữa bỏ các chữ như Bài 1 bài 2 và tiếp tục cho đến bài cuối khi bạn trả về tôi chỉ cần mỗi ĐỊNH DẠNH CÂU HỎI:CÂU TRẢ LỜI cho các bài ở dạng tầm bình thường thôi đừng khó quá vì học sinh của tôi là người khiếm thị
bỏ tiêu đề của các bài bạn trả về đi lưu ý khi bạn trả về các câu hỏi thì có định dạng là Question:answer để tôi còn có dữ liệu để trả về nữa các câu hỏi và trả lời được ngăn cách nhau bằng kí tự ::: để tôi có thể phân biệt và lưu nó về file json""")
    qa_pairs = response.text.split(":::")
    qa_dict = {}
    
    folder_path = f'AI/question_folder/{name}/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, 'questions.json')


    for pair in qa_pairs:
        lines = pair.strip().split("\n")
        if len(lines) >= 2: 
            question = lines[0].replace("Question: ", "").strip()
            answer = lines[1].replace("Answer: ", "").strip()
            qa_dict[question] = answer

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(qa_dict, f, ensure_ascii=False, indent=4)

    print("Questions and answers saved to JSON:", file_path)
    speak(response.text)
def check_question_AI(question, answer, user_answer):
    genai.configure(api_key="AIzaSyDZKaDnvhAfcNVUfKJiDoGb1bHYNGyAFeA")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"""giả sử bạn là một giáo viên dạy toán. Đây là bài toán tôi đưa ra: Hãy giải bài toán: {question}. Kết quả học sinh gửi tôi là
 {answer} và kết quả đúng của câu hỏi là {answer}. Bạn hay kiểm tra nếu kết quả này là đúng hay sai. Nếu đúng không tạo câu trả lời mà chỉ in ra đúng, sai thì trả về các bước để khắc phúc nhưng không được nêu ra đáp án bạn nhắc nhở rằng bạn đang nói với học sinh của bạn
bằng cách xưng em chi tiết hơn nhé và cảm xúc như thầy trò nhé""")
def get_data_from_given_question_and_ask_AI(name):
    print(name)
    filepath = f"question_folder/{name}/questions.json"
    with open(filepath, 'r', encoding='utf-8') as f:
        qa_dict = json.load(f)


    for question, answer in qa_dict.items():
        speak(question) 