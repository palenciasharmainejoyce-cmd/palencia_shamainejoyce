import sqlite3

# Connect to database
connection = sqlite3.connect('students.db')
cursor = connection.cursor()

# Drop the old table para masigurong malilikha ito kasama ang source column
cursor.execute("DROP TABLE IF EXISTS students;")

# Create table with source column
cursor.execute('''
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        name TEXT NOT NULL,
        program TEXT NOT NULL,
        year INTEGER NOT NULL,
        section TEXT NOT NULL,
        source TEXT DEFAULT 'Local'
    )
''')

# 5 student records with 'Local' source
students_data = [
    ('24-00094', 'Sharmaine Joyce Palencia', 'BSIT', 3, 'B', 'Local'),
    ('24-00095', 'Hapee Malunes', 'BSIT', 3, 'B', 'Local'),
    ('24-00096', 'Jero Paca-oncis', 'BSIT', 3, 'B', 'Local'),
    ('24-00097', 'Missy Miranda', 'BSIT', 2, 'B', 'Local'),
    ('24-00098', 'Ruby Joy Molina', 'BSIT', 2, 'B', 'Local')
]

# Insert records into the students table with source
cursor.executemany(
    "INSERT INTO students (student_id, name, program, year, section, source) VALUES (?, ?, ?, ?, ?, ?)",
    students_data
)

connection.commit()
connection.close()

print("Database successfully re-initialized with source column!")