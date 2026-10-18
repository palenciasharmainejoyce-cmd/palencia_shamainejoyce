import requests

url = "https://palencia-shamainejoyce.onrender.com/courses"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("--- Courses Endpoint Data ---")
    print("Course Code:", data["code"])
    print("Course Name:", data["name"])
    print("Units:", data["units"])
else:
    print("Request failed.")
    print("Status Code:", response.status_code)