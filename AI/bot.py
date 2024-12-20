import random
from functions.keyboard.keyboards import speak
import google.generativeai as genai
import os
import json
from functions.resource_path.path import resource_path
import database.database as db

def generate_questions_from_a_name_AI(chapter, soluong, dokho):

    genai.configure(api_key="AIzaSyAtRaqjHzf1AgEaDK7qTC0HH62sk7Jp48Y")
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(f"""
Lưu ý dành riêng cho học sinh khiếm thị:

Các câu hỏi chỉ liên quan đến tính toán, không bao gồm lý thuyết hay tự luận dài dòng.
Chủ đề bài tập thuộc chương {chapter} trong sách Toán 6 hoặc các lớp Toán 7, Toán 8, Toán 9 thuộc bộ sách "Chân Trời Sáng Tạo" của Bộ Giáo dục Việt Nam.
Bài tập được xây dựng với định dạng rõ ràng, dễ hiểu, phù hợp với học sinh khiếm thị.
Định dạng yêu cầu:

Các câu hỏi và câu trả lời phải được phân cách bằng ký tự | với khoảng cách nhỏ ở hai bên.
Không sử dụng ký tự | ở nơi khác ngoại trừ phân cách giữa câu hỏi và câu trả lời.
Các ký tự toán học (cộng, trừ, nhân, chia) được viết dưới dạng chữ để đảm bảo học sinh dễ hiểu.
Câu trả lời bằng số giữ nguyên định dạng số (không đổi thành chữ).
Yêu cầu cụ thể:

Tạo {soluong} bài tập liên quan đến tính toán, không bao gồm lý thuyết hay giải thích dài dòng.
Độ khó bài tập: {dokho} (dễ hoặc trung bình).
Tránh các câu hỏi yêu cầu giải thích "tại sao" hoặc yêu cầu liệt kê.
Câu trả lời cần ngắn gọn, chính xác, không bao gồm dấu câu trong câu trả lời.
Không sử dụng tiêu đề như "Bài 1", chỉ trả về câu hỏi và câu trả lời đúng theo định dạng.
Ví dụ:

Question: Ba cộng bảy bằng bao nhiêu | Answer: 10
Question: Mười hai trừ năm bằng bao nhiêu | Answer: 7
Lưu ý đặc biệt:

Bài tập phải bám sát chương {chapter} trong sách và tránh các câu quá phức tạp.
Tối ưu độ rõ ràng, dễ hiểu để phù hợp với học sinh khiếm thị.
Kiểm tra kỹ câu trả lời trước khi trả về, đảm bảo mọi câu trả lời chính xác và khớp với câu hỏi.
Hãy tạo bài tập một cách nhanh chóng và hiệu quả!
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
                print(chapter, question, answer)
                db.insert_new_question(chapter, question, answer, dokho)
            except ValueError as e:
                print(f"Lỗi tách câu hỏi và câu trả lời: {e}")
        else:
            print(f"Dòng không hợp lệ (không chứa '|'): {line}")



def check_question_AI(question, answer, user_answer):
    genai.configure(api_key="AIzaSyAxoki6CsXdtMdWuSEwyXQ4tUGDNOLCIGA")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"""Giả sử bạn là một giáo viên dạy toán. Đây là bài toán tôi đưa ra: 
            Hãy giải bài toán: "{question}". Kết quả học sinh gửi tôi là "{user_answer}"
            và kết quả đúng của câu hỏi là "{answer}". Bạn hãy kiểm tra nếu kết quả này là đúng hay sai. 
            Nếu đúng, không tạo câu trả lời mà chỉ in ra 'Đúng' và nếu sai 'Sai' và để chữ 'Sai' ở đầu câu 
            thì trả về các bước để khắc phục nhưng không được nêu ra đáp án. Bạn nhắc nhở rằng 
            bạn đang nói với học sinh của bạn bằng cách xưng em chi tiết hơn nhé và cảm xúc như thầy trò nhé.
            Vậy học sinh của bạn liệt kê các câu trả lời sai trong câu trả lời đó thì bạn sẽ nói sao 
            với trường hợp đó. ĐẶC BIỆT NHỚ LÀ CHỈ RÕ ra các câu trả lời sai đó và nói tại sao, 
            chỉ trả về hai giá trị 'Đúng' và 'Sai' thôi không ừm gì hết. 
            Các câu trả lời đúng sai như 'CÓ' hoặc 'KHÔNG' học sinh của tôi trả lời phải hoặc đúng hoặc 2 từ đó không dấu thì nhận diện giúp tôi.HOẶC 'PHẢI' HOẶC 'KHÔNG' MÀ HỌC SINH TÔI TRẢ LỜI 'PHAI' hoặc 'phai' HOẶC 'KHONG' HOẶC 'HONG' thì cũng tính nhé. VÀ HÃY KIỂM TRA KẾT QUẢ CỦA HỌC SINH TÔI NHẬP VỚI KẾT QUẢ ĐÚNG VÌ CÓ MẤY LẦN HỌC SINH TÔI NHẬP ĐÚNG VỚI KẾT QUẢ ĐÚNG THÌ BẠN LẠI BẢO SAI
            VÍ DỤ CÁC CÂU CÓ DẤU PHẨY (LIỆT KÊ) NHƯ 5, 3, 2, 1 MÀ HỌC SINH TÔI TRẢ LỜI LÀ 5 3 2 1 THÌ BẠN HÃY CHO LÀ ĐÚNG NHÉ VÌ HỌC SINH TÔI CÓ THỂ KHÔNG BIẾT DẤU PHẨY Ở ĐÂU MÀ CHỈ BIẾT DẤU CÁCH THÔI""")
    print(response.text)
    if response.text == "Đúng":
        return True, response.text
    elif "Sai" in response.text:
        return False,response.text  

