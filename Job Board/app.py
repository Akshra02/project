from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------------- DB Connection ----------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # change if needed
        password="Ash@2007", # your MySQL password
        database="job_board" # your DB name
    )

# ---------------- Front Page / Available Jobs ----------------
@app.route('/', methods=['GET'])
def index():
    search = request.args.get('search', '')
    location = request.args.get('location', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if search or location:
        query = "SELECT * FROM job WHERE title LIKE %s OR company LIKE %s"
        cursor.execute(query, (f"%{search}%", f"%{location}%"))
    else:
        cursor.execute("SELECT * FROM job")
    jobs = cursor.fetchall()
    conn.close()

    return render_template('index.html', jobs=jobs)

# ---------------- Register ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']   # role capture: user / company

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (name, email, password, role)
        )
        
        conn.commit()
        conn.close()
        flash("Registered Successfully! Please login.")
        
        return redirect(url_for('login'))
    return render_template('register.html')

# ---------------- Login ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Admin hardcoded login
        if email == "admin@gmail.com" and password == "admin123":
            session['user_id'] = 0
            session['name'] = "Admin"
            session['role'] = "admin"
            return redirect(url_for('admin_dashboard'))

        # Check DB
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']

            if user['role'] == 'user':
                return redirect(url_for('dashboard'))
            elif user['role'] == 'company':
                return redirect(url_for('company_dashboard'))
        else:
            flash("Invalid Credentials!")
            return redirect(url_for('login'))

    return render_template('login.html')

# ---------------- User Dashboard ----------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session and session.get('role') == 'user':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM job WHERE status='approved' OR status IS NULL")
        jobs = cursor.fetchall()
        conn.close()
        return render_template("dashboard.html", name=session['name'], jobs=jobs)
    return redirect(url_for('login'))

# ---------------- Company Dashboard ----------------
@app.route('/company')
def company_dashboard():
    if 'user_id' in session and session.get('role') == 'company':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM job WHERE company=(SELECT name FROM users WHERE id=%s)", (session['user_id'],))
        jobs = cursor.fetchall()
        conn.close()
        return render_template("company.html", name=session['name'], jobs=jobs)
    return redirect(url_for('login'))

# ---------------- Admin Dashboard ----------------
@app.route('/admin')
def admin_dashboard():
    if 'user_id' in session and session.get('role') == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM job")
        jobs = cursor.fetchall()
        conn.close()
        return render_template("admin.html", name=session['name'], jobs=jobs)
    return redirect(url_for('login'))

# ---------------- Apply Job ----------------
@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply_job(job_id):
    if 'user_id' not in session:
        flash("Please login to apply for jobs.")
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Save resume
        education = request.form.get('education')
        experience = request.form.get('experience')
        skills = request.form.get('skills')
        languages = request.form.get('languages')
        certifications = request.form.get('certifications')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO resumes (user_id, job_id, education, experience, skills, languages, certifications) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (session['user_id'], job_id, education, experience, skills, languages, certifications)
        )
        cursor.execute("INSERT INTO applications (user_id, job_id) VALUES (%s, %s)", 
                       (session['user_id'], job_id))
        conn.commit()
        conn.close()

        flash("Applied Successfully with Resume ✅")
        return redirect(url_for('dashboard'))

    # If GET → show resume form
    return render_template("resume_form.html", job_id=job_id)

# ---------------- Post Job (Company) ----------------
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'user_id' in session and session.get('role') == 'company':
        if request.method == 'POST':
            title = request.form['title']
            company = session['name']   # company name from login
            description = request.form['description']
            salary = request.form['salary']
            work_mode = request.form['work_mode']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO job (title, company, description, salary, work_mode, status) 
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (title, company, description, salary, work_mode, "pending"))
            conn.commit()
            conn.close()

            flash("Job Posted Successfully! Waiting for admin approval ✅")
            return redirect(url_for('company_dashboard'))
        return render_template('post_job.html')
    return redirect(url_for('login'))

# ---------------- Reject Job (Admin) ----------------
@app.route('/reject/<int:job_id>', methods=['POST'])
def reject_job(job_id):
    if 'user_id' in session and session.get('role') == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE job SET status = 'rejected' WHERE id=%s", (job_id,))
        conn.commit()
        conn.close()
        flash("Job Rejected Successfully!")
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

# ---------------- Approve Job (Admin) ----------------
@app.route('/approve/<int:job_id>', methods=['POST'])
def approve_job(job_id):
    if 'user_id' in session and session.get('role') == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE job SET status = 'approved' WHERE id=%s", (job_id,))
        conn.commit()
        conn.close()
        flash("Job Approved Successfully!")
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

# ---------------- Logout ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ---------------- Run App ----------------
if __name__ == '__main__':
    app.run(debug=True)
