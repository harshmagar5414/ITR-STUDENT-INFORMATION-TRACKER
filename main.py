from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "erp_secret_key"


# =========================
# DATABASE CONNECTION
# =========================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# AUTH PAGES
# =========================

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        cursor.execute("""
            INSERT INTO users(fullname, username, email, password, role)
            VALUES (?, ?, ?, ?, ?)
        """, (fullname, username, email, password, role))

        conn.commit()
        conn.close()

        flash("Registered Successfully")
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():

    conn = get_db()
    cursor = conn.cursor()

    username = request.form["username"]
    password = request.form["password"]

    cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    if user:

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]

        if user["role"] == "Admin":
            return redirect(url_for("admin_dashboard"))
        elif user["role"] == "Teacher":
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

    conn = get_db()
    cursor = conn.cursor()

    search = request.args.get("search")

    if search:
        cursor.execute("""
            SELECT * FROM students
            WHERE student_id LIKE ?
            OR fullname LIKE ?
        """, ("%" + search + "%", "%" + search + "%"))
    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()
    conn.close()

    return render_template("admin/students.html", students=students)


# =========================
# TEACHERS (ADMIN)
# =========================
@app.route("/teachers")
def teachers():

    conn = get_db()
    cursor = conn.cursor()

    search = request.args.get("search")

    if search:
        cursor.execute("""
            SELECT * FROM teachers
            WHERE teacher_id LIKE ?
            OR fullname LIKE ?
        """, ("%" + search + "%", "%" + search + "%"))
    else:
        cursor.execute("SELECT * FROM teachers")

    teachers = cursor.fetchall()
    conn.close()

    return render_template("admin/teachers.html", teachers=teachers)


# =========================
# COURSES
# =========================
@app.route("/courses", methods=["GET", "POST"])
def courses():

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("""
            INSERT INTO courses(course_code, course_name, department, semester, credits, faculty)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            request.form["course_code"],
            request.form["course_name"],
            request.form["department"],
            request.form["semester"],
            request.form["credits"],
            request.form["faculty"]
        ))

        conn.commit()

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    conn.close()

    return render_template("admin/courses.html", courses=courses)


# =========================
# MARKS
# =========================
@app.route("/marks", methods=["GET", "POST"])
def marks():

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("""
            INSERT INTO marks(student_id, student_name, department, semester, subject,
                              max_marks, obtained_marks, grade, result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form["student_id"],
            request.form["student_name"],
            request.form["department"],
            request.form["semester"],
            request.form["subject"],
            request.form["max_marks"],
            request.form["obtained_marks"],
            request.form["grade"],
            request.form["result"]
        ))

        conn.commit()

    cursor.execute("SELECT * FROM marks")
    marks = cursor.fetchall()

    conn.close()

    return render_template("admin/marks.html", marks=marks)


# =========================
# FEES
# =========================
@app.route("/fees", methods=["GET", "POST"])
def fees():

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("""
            INSERT INTO fees(student_id, student_name, department, academic_year,
                             total_fee, paid_fee, remaining_fee,
                             payment_date, payment_mode, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form["student_id"],
            request.form["student_name"],
            request.form["department"],
            request.form["academic_year"],
            request.form["total_fee"],
            request.form["paid_fee"],
            request.form["remaining_fee"],
            request.form["payment_date"],
            request.form["payment_mode"],
            request.form["status"]
        ))

        conn.commit()

    cursor.execute("SELECT * FROM fees")
    fees = cursor.fetchall()

    conn.close()

    return render_template("admin/fees.html", fees=fees)


# =========================
# NOTICES
# =========================
@app.route("/notices", methods=["GET", "POST"])
def notices():

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("""
            INSERT INTO notices(title, notice_date, audience, priority, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.form["title"],
            request.form["notice_date"],
            request.form["audience"],
            request.form["priority"],
            request.form["description"]
        ))

        conn.commit()

    cursor.execute("SELECT * FROM notices")
    notices = cursor.fetchall()

    conn.close()

    return render_template("admin/notices.html", notices=notices)


# =========================
# REPORTS
# =========================
@app.route("/reports")
def reports():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM courses")
    total_courses = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM marks")
    total_marks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM fees")
    total_fees = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM notices")
    total_notices = cursor.fetchone()[0]

    conn.close()

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

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("DELETE FROM settings")

        cursor.execute("""
            INSERT INTO settings(institute_name, email, phone, academic_year, principal, address, theme)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form["institute_name"],
            request.form["email"],
            request.form["phone"],
            request.form["academic_year"],
            request.form["principal"],
            request.form["address"],
            request.form["theme"]
        ))

        conn.commit()

    cursor.execute("SELECT * FROM settings LIMIT 1")
    settings = cursor.fetchone()

    conn.close()

    return render_template("admin/settings.html", settings=settings)


# =========================
# TEACHER MODULES
# =========================
@app.route("/teacher_dashboard")
def teacher_dashboard():
    return render_template("teacher/dashboard.html")


@app.route("/assignment", methods=["GET", "POST"])
def assignment():

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("""
            INSERT INTO assignments(course, subject, title, due_date, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request.form["course"],
            request.form["subject"],
            request.form["title"],
            request.form["due_date"],
            request.form["description"]
        ))

        conn.commit()

    cursor.execute("SELECT * FROM assignments")
    assignments = cursor.fetchall()

    conn.close()

    return render_template("teacher/assignment.html", assignments=assignments)


# =========================
# STUDENT DASHBOARD
# =========================
@app.route("/student_dashboard")
def student_dashboard():
    return render_template("student/dashboard.html")


@app.route("/student/profile")
def student_profile():

    conn = get_db()
    cursor = conn.cursor()

    student_id = session["user_id"]

    cursor.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    student = cursor.fetchone()

    conn.close()

    return render_template("student/profile.html", student=student)


@app.route("/student/marks")
def student_marks():

    conn = get_db()
    cursor = conn.cursor()

    student_id = session["user_id"]

    cursor.execute("SELECT * FROM marks WHERE student_id=?", (student_id,))
    marks = cursor.fetchall()

    conn.close()

    return render_template("student/marks.html", marks=marks)


@app.route("/student/fees")
def student_fees():

    conn = get_db()
    cursor = conn.cursor()

    student_id = session["user_id"]

    cursor.execute("SELECT * FROM fees WHERE student_id=?", (student_id,))
    fees = cursor.fetchall()

    conn.close()

    return render_template("student/fees.html", fees=fees)


@app.route("/student/courses")
def student_courses():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    conn.close()

    return render_template("student/courses.html", courses=courses)


@app.route("/student/notices")
def student_notices():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM notices
        WHERE audience='Students' OR audience='All'
    """)

    notices = cursor.fetchall()

    conn.close()

    return render_template("student/notices.html", notices=notices)


@app.route("/student/attendance")
def student_attendance():

    conn = get_db()
    cursor = conn.cursor()

    student_id = session["user_id"]

    cursor.execute("""
        SELECT * FROM attendance
        WHERE student_id=?
    """, (student_id,))

    attendance = cursor.fetchall()

    conn.close()

    return render_template("student/attendance.html", attendance=attendance)


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)