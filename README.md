# Assessment Management System

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0+-brightgreen.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-2.0+-orange.svg)](https://www.sqlalchemy.org/)
[![JWT](https://img.shields.io/badge/jwt-brightgreen.svg)](https://jwt.io/)

This web application provides a secure platform for managing student applications with role-based access control.

## Overview

This system is designed to streamline the student application process, providing a secure and user-friendly interface for both students and administrators. Key features include user authentication, application submission and tracking, PDF admission letter generation, role-based dashboard access, and file upload capabilities.

## Features

- **User Authentication:** Secure login/logout functionality for admins and students using Flask-Login and JWT.
- **Role-Based Access:** Separate dashboards and functionalities tailored for admins and students.
- **Application Management:** Students can submit, view, and update their applications. Admins can manage and review applications.
- **PDF Generation:** Automatically generate admission letters in PDF format using ReportLab.
- **File Uploads:** Secure handling of student documents like ID proof and degree certificates.
- **Admin Dashboard:** View all applications, approve/reject applications, and generate admission letters.
- **Student Dashboard:** Submit new applications, view submitted application status, and download admission letters (if approved).

## Getting Started

### Prerequisites

- Python 3.11+
- Flask 3.0+
- Flask-Login
- Flask-JWT-Extended
- Flask-WTF
- SQLAlchemy 2.0+
- ReportLab for PDF generation

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/abishekmukesh/application_submission.git
    cd assessment
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate    # Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Create a `.env` file** in the root directory of the project with the following structure:

    ```env
    SECRET_KEY=your_secret_key_here
    JWT_SECRET_KEY=your_jwt_secret_key_here
    SQLALCHEMY_DATABASE_URI=sqlite:///site.db
    ```

    -   Replace `your_secret_key_here` and `your_jwt_secret_key_here` with your actual secret keys.
    -   `SQLALCHEMY_DATABASE_URI` specifies the database to use (default is SQLite).

2.  **Load environment variables:**

    ```bash
    source .env  # Linux/Mac
    .env\Scripts\activate # Windows (using dotenv)
    ```

### Database Setup

1.  **Initialize the database:**
    ```bash
    python .\database\init_db.py
    ```

    This command initializes the database and automatically creates an admin account with username: `admin` and password: `admin123`.

### Running the Application

```bash
python app.py
```

# Accessing and Using the Assessment Management System

## Access

**Access the application at:** http://localhost:5000

## Authentication

### Admin Login
*   **URL:** `/admin/login`
*   **Username:** `admin`
*   **Password:** `admin123`

### Student Login
*   **URL:** `/student/login`
*   Use your registered roll number and password.

### Student Signup
*   **URL:** `/student/signup`

## Usage

### Admin Dashboard

*   View all applications
*   Approve/reject applications
*   Generate admission letters

### Student Dashboard

*   Submit new applications
*   View submitted application status
*   Download admission letters (if approved)

## Troubleshooting

*   **Clear Browser Cookies:** If you're having login issues, try clearing your browser cookies.
*   **Database Reset:** Use `python -m flask reset-db` to recreate the database.
*   **Incognito Mode:** Test authentication flows in incognito mode to avoid cached data issues.

## Development Notes

*   Use `debug=True` only in a development environment.
*   Never commit sensitive information (like secret keys) to version control.
*   Regularly update dependencies with `pip install --upgrade`.


## Contact

For questions or support: serabishek@gmail.com


