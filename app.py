from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector


app = Flask(__name__)

# MySQL configurations
db_config = {
    'host': '127.0.0.1',
    'user': 'flaskappuser',
    'password': 'Mysql123',
    'database': 'flaskdb',
}

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

db = SQLAlchemy(app)

# Student Model

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, default=0.0)

    def __init__(self, student_id, first_name, last_name, dob, amount_due):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.amount_due = amount_due

# REST APIs
@app.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(**data)

    db.session.add(new_student)
    db.session.commit()

    return jsonify({'message': 'Student added successfully'})


@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = [
        {
            'student_id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'dob': student.dob.isoformat(),
            'amount_due': student.amount_due
        }
        for student in students
    ]
    return jsonify(result)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
