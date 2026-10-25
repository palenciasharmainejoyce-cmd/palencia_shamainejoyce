import sqlite3
from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)


# Database connection helper
def get_db_connection():
  conn = sqlite3.connect("students.db")
  conn.row_factory = sqlite3.Row
  return conn


# Initialize SQLite database with 'source' column tracking
def init_db():
  conn = get_db_connection()
  conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            year INTEGER NOT NULL,
            section TEXT NOT NULL,
            source TEXT DEFAULT 'Local'
        )
    """)
  conn.commit()
  conn.close()


init_db()


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/student", methods=["GET"])
def get_student_info():
  return jsonify({
      "student_id": "24-00094",
      "name": "Sharmaine Joyce Palencia",
      "program": "BSIT",
      "year": 2,
      "section": "B",
  })


@app.route("/hello", methods=["GET"])
def say_hello():
  name = request.args.get("name", "Guest")
  return jsonify({"message": f"Hello, {name}! Welcome to Lab 9 API."})


@app.route("/courses", methods=["GET"])
def get_courses():
  return jsonify({
      "code": "IT 112",
      "name": "Information Technology Integration and Architecture",
      "units": 3,
  })


# GET all students or POST a new student (Local, External, or Partner)
@app.route("/api/students", methods=["GET", "POST"])
def handle_students():
  conn = get_db_connection()
  cursor = conn.cursor()

  if request.method == "GET":
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    students = [dict(row) for row in rows]
    return jsonify(students)

  elif request.method == "POST":
    data = request.get_json()
    student_id = data.get("student_id")
    name = data.get("name")
    program = data.get("program")
    year = data.get("year")
    section = data.get("section")
    source = data.get("source", "Local")

    cursor.execute(
        """
        INSERT INTO students (student_id, name, program, year, section, source)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (student_id, name, program, year, section, source),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return (
        jsonify({
            "message": "Student added successfully.",
            "student": {
                "id": new_id,
                "student_id": student_id,
                "name": name,
                "program": program,
                "year": year,
                "section": section,
                "source": source,
            },
        }),
        201,
    )


# PUT / UPDATE student record
@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
  data = request.get_json()
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
      """
      UPDATE students
      SET student_id = ?, name = ?, program = ?, year = ?, section = ?
      WHERE id = ?
  """,
      (
          data.get("student_id"),
          data.get("name"),
          data.get("program"),
          data.get("year"),
          data.get("section"),
          id,
      ),
  )
  conn.commit()
  conn.close()
  return jsonify({"message": "Student updated successfully!"})


# DELETE student record
@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("DELETE FROM students WHERE id = ?", (id,))
  conn.commit()
  conn.close()
  return jsonify({"message": "Student deleted successfully!"})


# Filter students by section
@app.route("/students/section/<section_name>", methods=["GET"])
def get_students_by_section(section_name):
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM students WHERE section = ?", (section_name,))
  rows = cursor.fetchall()
  conn.close()
  students = [dict(row) for row in rows]
  return jsonify(students)


# Retrieve Partner Records from Missy's Live API
@app.route("/partner-records", methods=["GET"])
def get_partner_records():
  partner_url = "https://act-8-miranda-2.onrender.com/api/students"
  try:
    response = requests.get(partner_url, timeout=10)
    if response.status_code == 200:
      return jsonify(response.json())
    return jsonify([]), response.status_code
  except Exception as e:
    return jsonify({"error": str(e)}), 500


# Import and Save Partner Record locally with 'Classmate API' source badge
@app.route("/import-student", methods=["POST"])
def import_student():
  data = request.get_json()
  student_id = data.get("student_id") or data.get("id")
  name = data.get("name")
  program = data.get("program")
  year = data.get("year")
  section = data.get("section")
  source = "Classmate API"

  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
      """
      INSERT INTO students (student_id, name, program, year, section, source)
      VALUES (?, ?, ?, ?, ?, ?)
  """,
      (student_id, name, program, year, section, source),
  )
  conn.commit()
  conn.close()

  return jsonify({"message": "Remote record saved successfully!"}), 201


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)