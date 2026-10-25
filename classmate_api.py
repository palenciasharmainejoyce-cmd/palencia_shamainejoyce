import requests

CLASSMATE_BASE_URL = "https://act-8-miranda-2.onrender.com"
ENDPOINT = "/api/students"

url = f"{CLASSMATE_BASE_URL}{ENDPOINT}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("--- Classmate's API Response (Miranda) ---")
    if isinstance(data, list):
        for student in data:
            print(f"ID: {student.get('student_id')} | Name: {student.get('name')} | Program: {student.get('program')}")
    else:
        print("Data:", data)
else:
    print("Request failed.")
    print("Status Code:", response.status_code)