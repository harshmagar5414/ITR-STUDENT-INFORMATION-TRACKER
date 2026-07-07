from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# MySQL table options
MYSQL_CHARSET = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = MYSQL_CHARSET
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Admin, Teacher, Student


class Student(db.Model):
    __tablename__ = "students"
    __table_args__ = MYSQL_CHARSET
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), unique=True, nullable=False)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    semester = db.Column(db.Integer)
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)


class Teacher(db.Model):
    __tablename__ = "teachers"
    __table_args__ = MYSQL_CHARSET
    
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(100), unique=True, nullable=False)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    qualification = db.Column(db.String(255))
    address = db.Column(db.Text)


class Course(db.Model):
    __tablename__ = "courses"
    __table_args__ = MYSQL_CHARSET
    
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50), unique=True, nullable=False)
    course_name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(100))
    semester = db.Column(db.Integer)
    credits = db.Column(db.Float)
    faculty = db.Column(db.String(255))


class Mark(db.Model):
    __tablename__ = "marks"
    __table_args__ = MYSQL_CHARSET
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False)
    student_name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(100))
    semester = db.Column(db.Integer)
    subject = db.Column(db.String(255))
    max_marks = db.Column(db.Float)
    obtained_marks = db.Column(db.Float)
    grade = db.Column(db.String(10))
    result = db.Column(db.String(50))


class Fee(db.Model):
    __tablename__ = "fees"
    __table_args__ = MYSQL_CHARSET
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False)
    student_name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(100))
    academic_year = db.Column(db.String(20))
    total_fee = db.Column(db.Float)
    paid_fee = db.Column(db.Float)
    remaining_fee = db.Column(db.Float)
    payment_date = db.Column(db.Date)
    payment_mode = db.Column(db.String(50))
    status = db.Column(db.String(50))


class Notice(db.Model):
    __tablename__ = "notices"
    __table_args__ = MYSQL_CHARSET
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    notice_date = db.Column(db.Date, default=datetime.now)
    audience = db.Column(db.String(100))  # Students, Teachers, All
    priority = db.Column(db.String(50))  # High, Medium, Low
    description = db.Column(db.Text)


class Assignment(db.Model):
    __tablename__ = "assignments"
    __table_args__ = MYSQL_CHARSET
    
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100))
    subject = db.Column(db.String(255))
    title = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.Date)
    description = db.Column(db.Text)


class Attendance(db.Model):
    __tablename__ = "attendance"
    __table_args__ = MYSQL_CHARSET
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, default=datetime.now)
    status = db.Column(db.String(50))  # Present, Absent
    remarks = db.Column(db.Text)


class Setting(db.Model):
    __tablename__ = "settings"
    __table_args__ = MYSQL_CHARSET
    
    id = db.Column(db.Integer, primary_key=True)
    institute_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    academic_year = db.Column(db.String(20))
    principal = db.Column(db.String(255))
    address = db.Column(db.Text)
    theme = db.Column(db.String(50))
