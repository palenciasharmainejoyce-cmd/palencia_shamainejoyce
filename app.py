from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to Sharmaine's API!"


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
                "code": "IT3120",
                "name": "System Integration",
                "units": 3
    })

@app.route('/sharmaine')
def say_sharmaine():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Gwapa si, {name}!"
    })

if __name__ == '__main__':
    app.run(debug=True)
