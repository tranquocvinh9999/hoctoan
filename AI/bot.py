import random
from functions.keyboard.keyboards import speak
from AI.functions.math import nhan, cong, tru
from functions.keyboard.keyboards import nhap_va_noi
import google.generativeai as genai
import os
import json

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

def generate_questions_from_a_name_AI(name, so_luong_cau_hoi):

    genai.configure(api_key="AIzaSyDZKaDnvhAfcNVUfKJiDoGb1bHYNGyAFeA")
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(f"""LƯU Ý ĐẦU TIÊN VÌ HỌC SINH CỦA TÔI LÀ NGƯỜI KHIẾM THỊ NÊN HÃY LÀM CÁC CÂU HỎI NẰM TRONG TẦM KIỂM SOÁT CỦA HỌ,Viết cho tôi các bài tập về tính toán chứ không được viết về kiểm tra lý thuyết nhé,Đây là chương của chủ đề của một bài trong sách toán sáu tên là {name} thuộc sách mới KẾT NỐI TRI THỨC 
của phòng giáo dục Việt Nam bạn hãy viết cho tôi {so_luong_cau_hoi} bài tập về bài đó giúp tôi để tôi cho các học sinh của tôi làm nữa lưu ý các bài tập có định dạng CÂU HỎI:CÂU TRẢ LỜI và lược bỏ các câu trả lời của bạn không cần thiết
bỏ các chữ in hoa khi bạn trả về text cho tôi nữa bỏ các chữ như Bài 1 bài 2 và tiếp tục cho đến bài cuối khi bạn trả về tôi chỉ cần mỗi ĐỊNH DẠNH CÂU HỎI:CÂU TRẢ LỜI cho các bài ở dạng tầm bình thường thôi đừng khó quá vì học sinh của tôi là người khiếm thị
bỏ tiêu đề của các bài bạn trả về đi VÀ TÔI BẮT BUỘC PHẢI lưu ý VÀ CỐ ĐỊNH khi bạn trả về các câu hỏi thì có định dạng là Question:answer để tôi còn có dữ liệu để trả về nữa các câu hỏi và trả lời được ngăn cách nhau bằng kí tự | để tôi có thể phân biệt và lưu nó về file json
VÀ HÃY CHẮC CHẮN NHỮNG LẦN TRẢ VỀ KẾT QUẢ SAU CỦA BẠN HÃY LÀM GIỐNG NHƯ NÀY độ khó ở mức dễ vì học sinh tôi là người khiếm thị tôi không cần bạn phân tích TÔI CHỈ CẦN BẠN IN BÀI TẬP RA  VÀ CHỈ DÙNG | ĐỂ PHÂN CÁCH GIỮA CÂU HỎI VÀ CÂU TRẢ LỜI KHÔNG DÙNG | ĐỂ PHÂN CÁCH CÁC CÂU HỎI
VÀ HÃY CỐ ĐỊNH RẰNG NÓ CÓ ĐỊNH DẠNG QUESTIONS: | ANSWER: BỎ CÁC DẤU * ĐI
""")
    

    print(response.text)

    lines = response.text.strip().split('\n')
    data = []

    for line in lines:
        line = line.strip()
        if '|' in line:
            try:
                question, answer = line.split('|', 1)
                question = question.replace("Question:", "").strip()
                answer = answer.strip().replace("Answer:", "").lower().strip()
            # Append the question and answer as a dictionary to the list
                data.append({
                    "question": question,
                    "answer": answer
                })
            except ValueError as e:
                print(f"Lỗi tách câu hỏi và câu trả lời: {e}")
        else:
            print(f"Dòng không hợp lệ (không chứa '|'): {line}")

    json_file_path = f'AI/question_folder/{name}/questions.json'  

    folder_path = os.path.dirname(json_file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Các câu hỏi đã được lưu vào {json_file_path}")
    except PermissionError as e:
        print(f"Lỗi quyền truy cập khi ghi vào tệp: {e}")



def check_question_AI(question, answer, user_answer):
    genai.configure(api_key="AIzaSyDZKaDnvhAfcNVUfKJiDoGb1bHYNGyAFeA")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"""giả sử bạn là một giáo viên dạy toán. Đây là bài toán tôi đưa ra: Hãy giải bài toán: {question}. Kết quả học sinh gửi tôi là
 {user_answer} và kết quả đúng của câu hỏi là {answer}. Bạn hay kiểm tra nếu kết quả này là đúng hay sai. Nếu đúng không tạo câu trả lời mà chỉ in ra đúng, sai thì trả về các bước để khắc phúc nhưng không được nêu ra đáp án bạn nhắc nhở rằng bạn đang nói với học sinh của bạn
bằng cách xưng em chi tiết hơn nhé và cảm xúc như thầy trò nhé và đặc biệt phải nhớ rằng bạn hãy nói có cảm xúc như thầy trò nhé vậy học sinh của bạn liệt kê các câu trả lời sai trong câu trả lời đó thì bạn sẽ nói sao với trường hợp đó
ĐẶC BIỆT NHỚ LÀ CHỈ RÕ ra các câu trả lời sai đó và nói tại sao""")
    print(response.text)
    if response.text == "Đúng":
        return True, response.text
    elif "Sai" in response.text:
        return False,response.text  

def get_data_from_given_question_and_ask_AI(name):
    correct_answer = 0
    wrong_answer = 0
    score = 0
    print(name)
    name_remove_space = name.replace(" ", "")
    filepath = f"AI/question_folder/{name}/questions.json"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        qa_dict = json.load(f)

    for question, answer in qa_dict.items():
        speak(question) 
        while True:
            user_answer = nhap_va_noi("Nhập câu trả lời của bạn").strip()

            result = check_question_AI(question, answer, user_answer)
            
            if result is not None:
                is_correct, response_message = result
                
                if is_correct:
                    speak("Đúng rồi")
                    correct_answer+=1
                    score += 1
                    break  
                else:
                    if response_message: 
                        speak(response_message)
                        wrong_answer += 1
                    else:
                        speak("Có lỗi xảy ra, không có thông tin để nói.")
            else:
                speak("Có lỗi xảy ra khi kiểm tra câu trả lời.")
    return correct_answer, wrong_answer, score