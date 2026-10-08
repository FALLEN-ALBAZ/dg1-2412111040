import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Xác định đường dẫn tuyệt đối tới file students.json
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'students.json')
# xin chao
def read_students():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_students(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- Câu C1 ---
@app.route('/', methods=['GET'])
def index():
    students = read_students()
    return render_template('index.html', students=students)

# --- Câu C2 ---
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "student": "2412111040"}), 200

@app.route('/api/students', methods=['GET'])
def get_students():
    students = read_students()
    lop_filter = request.args.get('lop')
    if lop_filter:
        students = [s for s in students if s.get('lop') == lop_filter]
    return jsonify(students), 200

@app.route('/api/students/<int:id>', methods=['GET'])
def get_student_by_id(id):
    students = read_students()
    for s in students:
        if s.get('id') == id:
            return jsonify(s), 200
    return jsonify({"error": "Student not found"}), 404

# --- Câu C3 ---
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad request"}), 400

    # Kiểm tra thiếu trường bắt buộc
    required_fields = ['mssv', 'ho_ten', 'lop', 'diem']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Kiểm tra điểm trong khoảng 0-10
    try:
        diem = float(data['diem'])
        if diem < 0 or diem > 10:
            return jsonify({"error": "Diem must be between 0 and 10"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid diem format"}), 400

    students = read_students()

    # Tự sinh id kế tiếp
    new_id = max([s.get('id', 0) for s in students], default=0) + 1
    # Danh sách học sinh kế tiếp
    new_student = {   
        "id": new_id,
        "mssv": str(data['mssv']),
        "ho_ten": str(data['ho_ten']),
        "lop": str(data['lop']),
        "diem": diem
    }

    students.append(new_student)
    write_students(students)

    return jsonify(new_student), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
