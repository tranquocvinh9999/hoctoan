import random
from functions.keyboard.keyboards import speak
import google.generativeai as genai
import os
import json
from functions.resource_path.path import resource_path


def generate_questions_from_a_name_AI(name, so_luong_cau_hoi):

    genai.configure(api_key="AIzaSyAxoki6CsXdtMdWuSEwyXQ4tUGDNOLCIGA")
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(f"""LƯU Ý ĐẦU TIÊN VÌ HỌC SINH CỦA TÔI LÀ NGƯỜI KHIẾM THỊ NÊN HÃY LÀM CÁC CÂU HỎI NẰM TRONG TẦM KIỂM SOÁT CỦA HỌ,Viết cho tôi các bài tập về tính toán chứ không được viết về kiểm tra lý thuyết nhé,Đây là chương của chủ đề của một bài trong sách toán sáu tên là {name} thuộc sách mới KẾT NỐI TRI THỨC 
của phòng giáo dục Việt Nam bạn hãy viết cho tôi {so_luong_cau_hoi} bài tập về bài đó giúp tôi để tôi cho các học sinh của tôi làm nữa lưu ý các bài tập có định dạng CÂU HỎI:CÂU TRẢ LỜI và lược bỏ các câu trả lời của bạn không cần thiết
bỏ các chữ in hoa khi bạn trả về text cho tôi nữa bỏ các chữ như Bài 1 bài 2 và tiếp tục cho đến bài cuối khi bạn trả về tôi chỉ cần mỗi ĐỊNH DẠNH CÂU HỎI:CÂU TRẢ LỜI cho các bài ở dạng tầm bình thường thôi đừng khó quá vì học sinh của tôi là người khiếm thị
bỏ tiêu đề của các bài bạn trả về đi VÀ TÔI BẮT BUỘC PHẢI lưu ý VÀ CỐ ĐỊNH khi bạn trả về các câu hỏi thì có định dạng là Question:answer để tôi còn có dữ liệu để trả về nữa các câu hỏi và trả lời được ngăn cách nhau bằng kí tự | để tôi có thể phân biệt và lưu nó về file json
VÀ HÃY CHẮC CHẮN NHỮNG LẦN TRẢ VỀ KẾT QUẢ SAU CỦA BẠN HÃY LÀM GIỐNG NHƯ NÀY độ khó ở mức dễ vì học sinh tôi là người khiếm thị tôi không cần bạn phân tích TÔI CHỈ CẦN BẠN IN BÀI TẬP RA  VÀ CHỈ DÙNG | ĐỂ PHÂN CÁCH GIỮA CÂU HỎI VÀ CÂU TRẢ LỜI KHÔNG DÙNG | ĐỂ PHÂN CÁCH CÁC CÂU HỎI
VÀ  BẮT BUỘC HÃY CỐ ĐỊNH RẰNG NÓ CÓ ĐỊNH DẠNG QUESTIONS: | ANSWER: BỎ CÁC DẤU * ĐI DẤU | NÊN ĐƯỢC CÁC RA DẤU CÁCH NHỎ ĐỂ MÁY TÔI CÓ THỂ PHÂN BIỆT VÀ TẢI VỀ, LƯU Ý ĐẶC BIỆT HỌC SINH CỦA TÔI LÀ NGƯỜI KHIÊM THỊ HỌ KHÔNG THỂ LÀM CÁC BÀI TOÁN KHÓ BẠN HÃY ĐƯA RA CÁC BÀI TOÁN ĐƠN GIẢN VÀ KHÔNG DÀI DÒNG Ở CÂU TRẢ LỜI, BỎ CÁC CÂU HỎI TẠI SAO
VÀ BẠN TẠO CÂU HỎI LÀM SAO ĐỂ CÂU TRẢ LỜI NGẮN NHẤT CÓ THỂ VÀ DỄ DÀNG NHẤT CỰC KÌ LƯU Ý CÁC CÂU HỎI CÓ MANG TÍNH TỰ LUẬN DÀI THÌ KHÔNG ĐƯỢC THÊM VÀO, LÀM SAO ĐỂ CÁC CÂU TRẢ LỜI TÔI NGẮN NHẤT CÓ THỂ, BỎ ĐI CÁC CHỮ KHÔNG LIÊN QUAN ĐẾN CÂU HỎI VÀ CÂU TRẢ LỜI.
VÍ DỤ CÁC CÂU HỎI PHẢI HOẶC KHÔNG PHẢI THÌ CÂU TRẢ LỜI CHỈ NÊN LÀ KHÔNG HOẶC LÀ PHẢI, BỎ ĐI CÁC CÂU HỎI PHẢI TRẢ LỜI VÌ SAO, MỘT CÂU TRẢ LỜI MÀ CÁC CHỮ CÁI TRONG ĐÓ ĐỀU CÓ DẤU THÌ XIN BẠN HÃY BỎ DẤU ĐI CHUYỂN THÀNH KHÔNG DẤU HẾT

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
                data.append({
                    "question": question,
                    "answer": answer
                })
            except ValueError as e:
                print(f"Lỗi tách câu hỏi và câu trả lời: {e}")
        else:
            print(f"Dòng không hợp lệ (không chứa '|'): {line}")

    json_file_path = f'AI/question_folder/{name}/questions.json'  

    folder_path = os.path.dirname(resource_path(json_file_path))
    if not os.path.exists(resource_path(folder_path)):
        os.makedirs(resource_path(folder_path))

    try:
        with open(resource_path(json_file_path), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Các câu hỏi đã được lưu vào {json_file_path}")
    except PermissionError as e:
        print(f"Lỗi quyền truy cập khi ghi vào tệp: {e}")



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

