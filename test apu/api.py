from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Đường dẫn tới file JSON lưu dữ liệu học sinh
data_file = "student_data.json"
output_file = "sorted_student_data.json"

# Đọc dữ liệu từ file JSON
def load_data():
    try:
        with open(data_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Lưu dữ liệu vào file JSON
def save_data(data, filename=data_file):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Xếp hạng và tính tổng cộng số lần đúng, sai, tổng điểm cho học sinh
def rank_and_calculate(data):
    for student, scores in data.items():
        correct = scores.get('correct', 0)
        total = scores.get('total', 0)
        accuracy = correct / total if total > 0 else 0

        # Xếp hạng dựa trên tỉ lệ trả lời đúng
        if accuracy >= 0.8:
            data[student]['rank'] = 'Tốt'
        elif accuracy >= 0.6:
            data[student]['rank'] = 'Khá'
        else:
            data[student]['rank'] = 'Trung Bình'

        # Tính tổng số lần đúng, sai và tổng điểm
        data[student]['total_correct'] = correct
        data[student]['total_incorrect'] = total - correct
        data[student]['total_score'] = correct

    return data

# Sắp xếp học sinh dựa trên tổng điểm từ cao xuống thấp
def sort_students(data):
    # Chuyển dữ liệu thành list và sắp xếp theo total_score
    sorted_data = sorted(data.items(), key=lambda x: x[1]['total_score'], reverse=True)
    
    # Trả về dưới dạng dictionary đã sắp xếp
    return dict(sorted_data)

# API để học sinh gửi điểm lên
@app.route('/submit_scores', methods=['POST'])
def submit_scores():
    student_name = request.json.get('name')
    correct = request.json.get('correct')
    total = request.json.get('total')

    if not student_name or correct is None or total is None:
        return jsonify({"error": "Thiếu dữ liệu"}), 400

    # Load dữ liệu hiện tại và cập nhật
    data = load_data()
    data[student_name] = {"correct": correct, "total": total}

    # Lưu lại dữ liệu
    save_data(data)
    return jsonify({"message": "Dữ liệu đã được lưu thành công"}), 200

# API để xếp hạng, tính tổng, sắp xếp và lưu kết quả vào file JSON khác
@app.route('/get_sorted_ranks', methods=['GET'])
def get_sorted_ranks():
    data = load_data()

    if not data:
        return jsonify({"error": "Không có dữ liệu"}), 404

    # Xếp hạng và tính tổng cộng
    ranked_data = rank_and_calculate(data)

    # Sắp xếp học sinh theo tổng điểm
    sorted_data = sort_students(ranked_data)

    # Lưu kết quả đã sắp xếp vào file JSON khác
    save_data(sorted_data, filename=output_file)

    return jsonify(sorted_data), 200

if __name__ == '__main__':
    app.run(debug=True)
