import openai

# Thiết lập API key từ OpenAI
openai.api_key = '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'

def get_correction(prompt):
    """
    Hàm này sẽ gửi bài toán tới GPT để kiểm tra và phát hiện lỗi
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Hoặc model="gpt-4" nếu bạn có quyền truy cập
        messages=[
            {"role": "system", "content": "You are an assistant that helps correct math problems."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
        n=1
    )
    return response['choices'][0]['message']['content'].strip()

def main():
    while True:
        # Nhập bài toán từ người dùng
        math_problem = input("Nhập bài toán hoặc giải pháp của bạn (hoặc 'thoát' để dừng): ")
        if math_problem.lower() == 'thoát':
            break

        # Tạo prompt để gửi yêu cầu tới GPT
        prompt = f"Phát hiện lỗi và gợi ý sửa cho bài toán sau: {math_problem}"
        
        # Gửi bài toán tới GPT để kiểm tra và phát hiện lỗi
        correction = get_correction(prompt)

        # In ra kết quả và gợi ý sửa lỗi
        print("Phân tích và gợi ý sửa lỗi:")
        print(correction)

if __name__ == "__main__":
    main()
