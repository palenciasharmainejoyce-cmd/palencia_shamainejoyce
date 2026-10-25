import sqlite3

# Connect to database (creates it if it doesn't exist)
connection = sqlite3.connect('students.db')
cursor = connection.cursor()

# Create table directly in Python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        program TEXT NOT NULL,
        section TEXT NOT NULL,
        student_id TEXT NOT NULL,
        year INTEGER NOT NULL
    )
''')

# 5 student records with at least two different sections & year levels
students_data = [
    ('Sharmaine Joyce Palencia', 'BSIT', 'B', '24-00094', 3),
    ('Hapee Malunes', 'BSIT', 'B', '24-00095', 3),
    ('Jero Paca-oncis', 'BSIT', 'B', '24-00096', 3),
    ('Missy Miranda', 'BSIT', 'B', '24-00097', 2),
    ('Ruby Joy Molina', 'BSIT', 'B', '24-00098', 2)
]

# Clear old records to avoid duplication
cursor.execute("DELETE FROM students;")

# Insert records into the students table
cursor.executemany(
    "INSERT INTO students (name, program, section, student_id, year) VALUES (?, ?, ?, ?, ?)",
    students_data
)

connection.commit()
connection.close()

print("Database successfully re-initialized with updated student records!")