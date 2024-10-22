
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

response = model.generate_content(f"""giả sử bạn là một giáo viên dạy toán. Đây là bài toán tôi đưa ra: Hãy giải bài toán: Hãy liệt kê tất cả các ước của số 12.. Kết quả học sinh gửi tôi là
 1 2 3 6 7 9 và kết quả đúng của câu hỏi là 1, 2, 3, 4, 6, 12.. Bạn hay kiểm tra nếu kết quả này là đúng hay sai. Nếu đúng không tạo câu trả lời mà chỉ in ra đúng, sai thì trả về các bước để khắc phúc nhưng không được nêu ra đáp án bạn nhắc nhở rằng bạn đang nói với học sinh của bạn
bằng cách xưng em chi tiết hơn nhé và đặc biệt phải nhớ rằng bạn hãy nói có cảm xúc như thầy trò nhé vậy học sinh của bạn liệt kê các câu trả lời sai trong câu trả lời đó thì bạn sẽ nói sao với trường hợp đó
ĐẶC BIỆT NHỚ LÀ CHỈ RÕ ra các câu trả lời sai đó và nói tại sao""")
print(response.text)