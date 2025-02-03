from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for,session
from werkzeug.security import check_password_hash
from models import Admin, Student
from forms import AdminLoginForm, StudentLoginForm, StudentSignupForm
from flask_login import login_user, logout_user,current_user
from flask_jwt_extended import create_access_token
from extensions import db
auth_bp = Blueprint('auth', __name__)

from flask_login import login_user

from flask_login import login_user

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    # If user is already logged in, redirect appropriately
    if current_user.is_authenticated:
        if isinstance(current_user, Admin):
            return redirect(url_for('admin_dashboard'))
        else:
            logout_user()  # Force logout if wrong user type

    if request.method == 'POST':
        admin = Admin.query.filter_by(username=request.form['username']).first()
        if admin and check_password_hash(admin.password, request.form['password']):
            login_user(admin)
            session['user_type'] = 'admin'  # Set session variable
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'error')
        return redirect(url_for('auth.admin_login'))
    form = AdminLoginForm()
    return render_template('admin_login.html', form=form)

@auth_bp.route('/student/login', methods=['GET', 'POST'])
def student_login():
    # If user is already logged in, redirect appropriately
    if current_user.is_authenticated:
        if isinstance(current_user, Student):
            return redirect(url_for('student_dashboard'))
        else:
            logout_user()  # Force logout if wrong user type

    if request.method == 'POST':
        student = Student.query.filter_by(roll_number=request.form['roll_number']).first()
        if student and check_password_hash(student.password, request.form['password']):
            login_user(student)
            session['user_type'] = 'student'  # Set session variable
            flash('Logged in successfully!', 'success')
            return redirect(url_for('student_dashboard'))
        flash('Invalid credentials', 'error')
        return redirect(url_for('auth.student_login'))
    form = StudentLoginForm()
    return render_template('student_login.html', form=form)

@auth_bp.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    form = StudentSignupForm()
    if form.validate_on_submit():
        existing = Student.query.filter_by(roll_number=form.roll_number.data).first()
        if existing:
            flash('Roll number already exists', 'error')
            return redirect(url_for('auth.student_signup'))
        student = Student(roll_number=form.roll_number.data)
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('auth.student_login'))
    return render_template('student_signup.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    session.clear()  # Clear all session data
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.student_login'))


@auth_bp.route('/student/forgot-password', methods=['GET', 'POST'])
def student_forgot_password():
    return "Forgot Password Page"  