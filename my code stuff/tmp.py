
import google.generativeai as genai
import os
from functions.keyboard.keyboards import speak
# abc = [
#     "1": "số 9 là số âm",
#     "2" "số 1 không được chia hết bởi các số khác"
# ]
# sosanh = [
#     "1": "số 9 là số dương",
#     "2": "số 1 được chia hết bởi các số khác"
# ]

genai.configure(api_key="AIzaSyDZKaDnvhAfcNVUfKJiDoGb1bHYNGyAFeA")
model = genai.GenerativeModel("gemini-1.5-flash")
    # response = model.generate_content(f"""giả sử bạn là một giáo viên dạy toán. Đây là bài toán tôi đưa ra: Hãy giải bài toán: x + 1 = 3. Kết quả học sinh gửi tôi là
    # x = 3. Bạn hay kiểm tra nếu kết quả này là đúng hay sai. Nếu đúng không tạo câu trả lời mà chỉ in ra đúng, sai thì trả về các bước để khắc phúc nhưng không được nêu ra đáp án""")
response = model.generate_content(f"""Đây là chương của chủ đề của một bài trong sách toán sáu tên là sốnguyêntố thuộc sách mới KẾT NỐI TRI THỨC 
của phòng giáo dục Việt Nam bạn hãy viết cho tôi 5 bài tập về bài đó giúp tôi để tôi cho các học sinh của tôi làm nữa lưu ý các bài tập có định dạng CÂU HỎI:CÂU TRẢ LỜI và lược bỏ các câu trả lời của bạn không cần thiết
bỏ các chữ in hoa khi bạn trả về text cho tôi nữa bỏ các chữ như Bài 1 bài 2 và tiếp tục cho đến bài cuối khi bạn trả về tôi chỉ cần mỗi ĐỊNH DẠNH CÂU HỎI:CÂU TRẢ LỜI cho các bài ở dạng tầm bình thường thôi đừng khó quá vì học sinh của tôi là người khiếm thị
bỏ tiêu đề của các bài bạn trả về đi VÀ TÔI BẮT BUỘC PHẢI lưu ý VÀ CỐ ĐỊNH khi bạn trả về các câu hỏi thì có định dạng là Question:answer để tôi còn có dữ liệu để trả về nữa các câu hỏi và trả lời được ngăn cách nhau bằng kí tự | để tôi có thể phân biệt và lưu nó về file json
VÀ HÃY CHẮC CHẮN NHỮNG LẦN TRẢ VỀ KẾT QUẢ SAU CỦA BẠN HÃY LÀM GIỐNG NHƯ NÀY độ khó ở mức dễ vì học sinh tôi là người khiếm thị tôi không cần bạn phân tích TÔI CHỈ CẦN BẠN IN BÀI TẬP RA  VÀ CHỈ DÙNG | ĐỂ PHÂN CÁCH GIỮA CÂU HỎI VÀ CÂU TRẢ LỜI KHÔNG DÙNG | ĐỂ PHÂN CÁCH CÁC CÂU HỎI
VÀ HÃY CỐ ĐỊNH RẰNG NÓ CÓ ĐỊNH DẠNG QUESTIONS: | ANSWER: 
""")
qa_pairs = response.text.split(":::")
print(response.text)
import json

def generate_questions_from_a_name_AI(chapter, num_of_exercises):
    # Giả lập một response_text như bạn đã đưa
    response_text = """
    Question:Liệt kê tất cả các ước của 12 | 1, 2, 3, 4, 6, 12
    Question:Số nào là số nguyên tố trong các số sau: 2, 4, 6, 8, 11 | 2, 11
    Question:Phân tích số 20 ra thừa số nguyên tố | 20 = 2 x 2 x 5 = 2^2 x 5
    Question:Tìm số nguyên tố p sao cho p + 2 và p + 4 cũng là số nguyên tố | p = 3
    Question:Có bao nhiêu số nguyên tố nhỏ hơn 10 | 4
    """

    # Tách từng dòng của response_text
    lines = response_text.strip().split('\n')

    # Tạo một dictionary để lưu câu hỏi và câu trả lời
    data = {}

    for line in lines:
        line = line.strip()  # Loại bỏ khoảng trắng ở đầu và cuối dòng
        if '|' in line:
            # Nếu trong dòng có ký tự '|', ta sẽ tách nó thành câu hỏi và câu trả lời
            try:
                question, answer = line.split('|', 1)  # Tách thành 2 phần
                question = question.replace("Question:", "").strip()  # Loại bỏ "Question:" và khoảng trắng
                answer = answer.strip()  # Loại bỏ khoảng trắng ở câu trả lời
                data[question] = answer  # Thêm câu hỏi và câu trả lời vào dictionary
            except ValueError as e:
                # Nếu có lỗi gì đó xảy ra trong quá trình tách, in ra lỗi
                print(f"Lỗi tách câu hỏi và câu trả lời: {e}")
        else:
            # Nếu dòng không chứa ký tự '|', cảnh báo về dòng không hợp lệ
            print(f"Dòng không hợp lệ (không chứa '|'): {line}")

    # Lưu kết quả vào file JSON
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # In ra để kiểm tra (nếu cần)
    print(json.dumps(data, ensure_ascii=False, indent=4))


# Hàm menu gọi hàm generate_questions_from_a_name_AI
def menu():
    chapter = "Chương 1"  # Ví dụ bạn chọn chương 1
    num_of_exercises = 5  # Ví dụ số lượng bài tập là 5
    generate_questions_from_a_name_AI(chapter, num_of_exercises)

# Chạy menu
menu()