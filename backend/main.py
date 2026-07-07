from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import config
from models import db, User, Student, Teacher, Course, Mark, Fee, Notice, Assignment, Attendance, Setting
from sqlalchemy import and_, or_
import os

app = Flask(__name__)

# =========================
# LOAD CONFIGURATION
# =========================
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

db.init_app(app)


# =========================
# AUTH PAGES
# =========================

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        new_user = User(
            fullname=fullname,
            username=username,
            email=email,
            password=password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registered Successfully")
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username, password=password).first()

    if user:

        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

        if user.role == "Admin":
            return redirect(url_for("admin_dashboard"))
        elif user.role == "Teacher":
            return redirect(url_for("teacher_dashboard"))
        else:
            return redirect(url_for("student_dashboard"))

    flash("Invalid Credentials")
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")


# =========================
# ADMIN DASHBOARD
# =========================
@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")


# =========================
# STUDENTS (ADMIN)
# =========================
@app.route("/students")
def students():

    search = request.args.get("search")

    if search:
        students = Student.query.filter(
            or_(
                Student.student_id.ilike(f"%{search}%"),
                Student.fullname.ilike(f"%{search}%")
            )
        ).all()
    else:
        students = Student.query.all()

    return render_template("admin/students.html", students=students)


# =========================
# TEACHERS (ADMIN)
# =========================
@app.route("/teachers")
def teachers():

    search = request.args.get("search")

    if search:
        teachers = Teacher.query.filter(
            or_(
                Teacher.teacher_id.ilike(f"%{search}%"),
                Teacher.fullname.ilike(f"%{search}%")
            )
        ).all()
    else:
        teachers = Teacher.query.all()

    return render_template("admin/teachers.html", teachers=teachers)


# =========================
# COURSES
# =========================
@app.route("/courses", methods=["GET", "POST"])
def courses():

    if request.method == "POST":

        new_course = Course(
            course_code=request.form["course_code"],
            course_name=request.form["course_name"],
            department=request.form["department"],
            semester=request.form["semester"],
            credits=request.form["credits"],
            faculty=request.form["faculty"]
        )

        db.session.add(new_course)
        db.session.commit()
        flash("Course added successfully")

    courses = Course.query.all()

    return render_template("admin/courses.html", courses=courses)


# =========================
# MARKS
# =========================
@app.route("/marks", methods=["GET", "POST"])
def marks():

    if request.method == "POST":

        new_mark = Mark(
            student_id=request.form["student_id"],
            student_name=request.form["student_name"],
            department=request.form["department"],
            semester=request.form["semester"],
            subject=request.form["subject"],
            max_marks=request.form["max_marks"],
            obtained_marks=request.form["obtained_marks"],
            grade=request.form["grade"],
            result=request.form["result"]
        )

        db.session.add(new_mark)
        db.session.commit()
        flash("Mark added successfully")

    marks = Mark.query.all()

    return render_template("admin/marks.html", marks=marks)


# =========================
# FEES
# =========================
@app.route("/fees", methods=["GET", "POST"])
def fees():

    if request.method == "POST":

        new_fee = Fee(
            student_id=request.form["student_id"],
            student_name=request.form["student_name"],
            department=request.form["department"],
            academic_year=request.form["academic_year"],
            total_fee=request.form["total_fee"],
            paid_fee=request.form["paid_fee"],
            remaining_fee=request.form["remaining_fee"],
            payment_date=request.form["payment_date"],
            payment_mode=request.form["payment_mode"],
            status=request.form["status"]
        )

        db.session.add(new_fee)
        db.session.commit()
        flash("Fee record added successfully")

    fees = Fee.query.all()

    return render_template("admin/fees.html", fees=fees)


# =========================
# NOTICES
# =========================
@app.route("/notices", methods=["GET", "POST"])
def notices():

    if request.method == "POST":

        new_notice = Notice(
            title=request.form["title"],
            notice_date=request.form["notice_date"],
            audience=request.form["audience"],
            priority=request.form["priority"],
            description=request.form["description"]
        )

        db.session.add(new_notice)
        db.session.commit()
        flash("Notice added successfully")

    notices = Notice.query.all()

    return render_template("admin/notices.html", notices=notices)


# =========================
# REPORTS
# =========================
@app.route("/reports")
def reports():

    total_students = Student.query.count()
    total_teachers = Teacher.query.count()
    total_courses = Course.query.count()
    total_marks = Mark.query.count()
    total_fees = Fee.query.count()
    total_notices = Notice.query.count()

    return render_template(
        "admin/reports.html",
        total_students=total_students,
        total_teachers=total_teachers,
        total_courses=total_courses,
        total_marks=total_marks,
        total_fees=total_fees,
        total_notices=total_notices
    )


# =========================
# SETTINGS
# =========================
@app.route("/settings", methods=["GET", "POST"])
def settings():

    if request.method == "POST":

        # Delete existing settings
        Setting.query.delete()

        new_setting = Setting(
            institute_name=request.form["institute_name"],
            email=request.form["email"],
            phone=request.form["phone"],
            academic_year=request.form["academic_year"],
            principal=request.form["principal"],
            address=request.form["address"],
            theme=request.form["theme"]
        )

        db.session.add(new_setting)
        db.session.commit()
        flash("Settings updated successfully")

    settings = Setting.query.first()

    return render_template("admin/settings.html", settings=settings)


# =========================
# TEACHER MODULES
# =========================
@app.route("/teacher_dashboard")
def teacher_dashboard():
    return render_template("teacher/dashboard.html")


@app.route("/assignment", methods=["GET", "POST"])
def assignment():

    if request.method == "POST":

        new_assignment = Assignment(
            course=request.form["course"],
            subject=request.form["subject"],
            title=request.form["title"],
            due_date=request.form["due_date"],
            description=request.form["description"]
        )

        db.session.add(new_assignment)
        db.session.commit()
        flash("Assignment added successfully")

    assignments = Assignment.query.all()

    return render_template("teacher/assignment.html", assignments=assignments)


# =========================
# STUDENT DASHBOARD
# =========================
@app.route("/student_dashboard")
def student_dashboard():
    return render_template("student/dashboard.html")


@app.route("/student/profile")
def student_profile():

    student_id = session.get("user_id")
    student = Student.query.filter_by(id=student_id).first()

    return render_template("student/profile.html", student=student)


@app.route("/student/marks")
def student_marks():

    student_id = session.get("user_id")
    marks = Mark.query.filter_by(student_id=student_id).all()

    return render_template("student/marks.html", marks=marks)


@app.route("/student/fees")
def student_fees():

    student_id = session.get("user_id")
    fees = Fee.query.filter_by(student_id=student_id).all()

    return render_template("student/fees.html", fees=fees)


@app.route("/student/courses")
def student_courses():

    courses = Course.query.all()

    return render_template("student/courses.html", courses=courses)


@app.route("/student/notices")
def student_notices():

    notices = Notice.query.filter(
        or_(
            Notice.audience == "Students",
            Notice.audience == "All"
        )
    ).all()

    return render_template("student/notices.html", notices=notices)


@app.route("/student/attendance")
def student_attendance():

    student_id = session.get("user_id")
    attendance = Attendance.query.filter_by(student_id=student_id).all()

    return render_template("student/attendance.html", attendance=attendance)


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)