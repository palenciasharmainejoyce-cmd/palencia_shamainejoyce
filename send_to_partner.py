import requests

# Missy's Render API URL
partner_url = "https://act-8-miranda-2.onrender.com/api/students"

record = {
    "student_id": "EXT-001",
    "name": "Sample Exchange Record",
    "program": "BSIT",
    "year": 1,
    "section": "A",
    "source": "Partner API"
}

try:
    response = requests.post(partner_url, json=record, timeout=15)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
except requests.RequestException as e:
    print("Error sending record to partner:", e)