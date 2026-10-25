import sqlite3
import requests
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00094",
        "name": "Sharmaine Joyce Palencia",
        "program": "BSIT",
        "year": 3,
        "section": "B"
    })

@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })

@app.route('/courses')
def get_courses():
    return jsonify({
        "code": "IT 3120",
        "name": "System Integration",
        "units": 3
    })

# --- Database Endpoints (Lab 7) ---

@app.route('/students')
def get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])

@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (id,)
    ).fetchone()
    conn.close()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))

# --- Additional Task Endpoint: Filter Students by Section ---
@app.route('/students/section/<string:section_name>')
def get_students_by_section(section_name):
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students WHERE section = ?', (section_name,)
    ).fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])


# ==========================================
# --- CRUD & API ENDPOINTS (Lab 8 & 9) ---
# ==========================================

@app.route('/api/students', methods=['GET'])
def api_students():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    # Lab 9 Step 8: Handle source for external/partner records
    source = data.get('source', 'External API')
    conn = get_db_connection()
    cursor = conn.execute(
        """INSERT INTO students 
        (student_id, name, program, year, section, source) 
        VALUES (?, ?, ?, ?, ?, ?)""",
        (data['student_id'], data['name'], data['program'], 
         data['year'], data['section'], source)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({"message": "Student added", "id": new_id}), 201

@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (id,)
    ).fetchone()
    conn.close()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        """UPDATE students SET student_id=?, name=?, program=?, 
        year=?, section=? WHERE id=?""",
        (data['student_id'], data['name'], data['program'], 
         data['year'], data['section'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student updated"})

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted"})


# ==========================================
# --- LABORATORY ACTIVITY 9 INTEGRATION ---
# ==========================================

@app.route('/partner-records')
def partner_records():
    partner_url = "https://act-8-miranda-2.onrender.com/api/students"
    try:
        response = requests.get(partner_url, timeout=15)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException:
        return jsonify({"error": "Unable to retrieve partner data"}), 502

@app.route('/import-student', methods=['POST'])
def import_student():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO students
        (student_id, name, program, year, section, source)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (data['student_id'], data['name'], data['program'],
         data['year'], data['section'], 'Classmate API')
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Remote record saved"}), 201


# ==========================================
# --- PROXY ENDPOINT FOR CLASSMATE API ---
# ==========================================

@app.route('/proxy-classmate')
def proxy_classmate():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400
    try:
        response = requests.get(target_url, timeout=15)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)