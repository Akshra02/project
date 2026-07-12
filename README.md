# 💼 Job Board Portal

A web-based **Job Board Portal** developed using **Flask, MySQL, HTML, CSS, and Bootstrap**. The application connects job seekers and companies through a centralized platform where companies can post jobs, users can apply with resumes, and administrators can manage job approvals.

---

## ✨ Features

### 👤 Job Seeker
- User Registration & Login
- Browse available jobs
- Search jobs by title or company
- Apply for jobs
- Submit resume details
- View approved job listings

### 🏢 Company
- Company Registration & Login
- Post new job openings
- View posted jobs
- Track job approval status

### 👨‍💼 Admin
- Secure Admin Login
- View all job postings
- Approve job postings
- Reject job postings
- Manage platform content

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- Bootstrap
- Jinja2 Templates

### Backend
- Python
- Flask

### Database
- MySQL

---

## 📂 Project Structure

```
Job-Board-Portal/
│── app.py
│── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── company.html
│   ├── admin.html
│   ├── post_job.html
│   └── resume_form.html
│
│── static/
│   ├── css/
│   ├── images/
│   └── js/
│
│── database/
│   └── job_board.sql
│
└── README.md
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/your-username/job-board-portal.git
```

### Navigate to the project folder

```bash
cd job-board-portal
```

### Install dependencies

```bash
pip install flask mysql-connector-python
```

### Configure MySQL

Create a MySQL database named:

```sql
job_board
```

Update the database configuration in `app.py`:

```python
host="localhost"
user="root"
password="your_password"
database="job_board"
```

### Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 🔑 Default Admin Credentials

| Email | Password |
|-------|----------|
| admin@gmail.com | admin123 |

> **Note:** These credentials are hardcoded for demonstration purposes.

---


## 📋 Application Workflow

1. Users register as **Job Seeker** or **Company**.
2. Companies post job openings.
3. Job postings remain **Pending**.
4. Admin reviews and approves/rejects jobs.
5. Approved jobs appear on the user dashboard.
6. Job seekers apply by submitting their resume details.
7. Applications are stored in the database.

---

## 🌟 Future Enhancements

- Password hashing
- Email verification
- Resume file upload (PDF/DOCX)
- Company profile management
- Application status tracking
- Job recommendations
- Pagination and filters
- REST API support

---

## 📄 License

This project is developed for educational and learning purposes.

---

## 👩‍💻 Author

**Akshra Nishanth**

B.Tech Information Technology
