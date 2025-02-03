from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory,session
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from models import Application, Admin, Student
from config import Config
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from extensions import db
from auth import auth_bp, logout_user
from flask_login import LoginManager, current_user, login_user, login_required
from decorators import admin_required, student_required
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.student_login'  # Set default login view
    app.register_blueprint(auth_bp)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id is None:
            return None
        
        # First try to get the user type from session
        user_type = session.get('user_type')
        
        if user_type == 'admin':
            return db.session.get(Admin, int(user_id))
        elif user_type == 'student':
            return db.session.get(Student, int(user_id))
        
        # If no user_type in session, return None to force re-login
        return None

    @app.route('/')
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.student_login'))
            
        if 'user_type' not in session:
            logout_user()
            return redirect(url_for('auth.student_login'))
            
        if session['user_type'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
            
    return app

app = create_app()
jwt = JWTManager(app)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class ApplicationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    degree = StringField('Degree', validators=[DataRequired()])
    university = StringField('University', validators=[DataRequired()])
    id_proof = FileField('ID Proof (PDF, JPG, PNG)', validators=[])
    degree_certificate = FileField('Degree Certificate (PDF, JPG, PNG)', validators=[])
    submit = SubmitField('Submit Application')


@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    applications = Application.query.all()
    return render_template('admin_dashboard.html', applications=applications)

@app.route('/student/dashboard')
@login_required
@student_required
def student_dashboard():
    application = Application.query.filter_by(user_id=current_user.id).first()
    form = ApplicationForm()
    return render_template('student_dashboard.html', application=application, form=form)
class AdminReviewForm(FlaskForm):
    status = SelectField('Status', choices=[('Approved', 'Approve'), ('Rejected', 'Reject')])
    submit = SubmitField('Update')


def generate_admission_letter(application):
    pdf_filename = os.path.join(app.root_path, 'pdfs', f"admission_letter_{application.id}.pdf")
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    title_style = styles['h1']
    title_style.alignment = 1
    story.append(Paragraph("Admission Letter", title_style))
    story.append(Spacer(1, 12))

    normal_style = styles['Normal']
    story.append(Paragraph(f"Dear {application.first_name} {application.last_name},", normal_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Congratulations! Your application for admission has been approved.", normal_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<strong>Details:</strong>", normal_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph(f"<strong>Name:</strong> {application.first_name} {application.last_name}", normal_style))
    story.append(Paragraph(f"<strong>Email:</strong> {application.email}", normal_style))
    story.append(Paragraph(f"<strong>Phone:</strong> {application.phone}", normal_style))
    story.append(Paragraph(f"<strong>Degree:</strong> {application.degree}", normal_style))
    story.append(Paragraph(f"<strong>University:</strong> {application.university}", normal_style))
    story.append(Paragraph(f"<strong>University:</strong> {application.degree_certificate}", normal_style))
    story.append(Paragraph(f"<strong>University:</strong> {application.id_proof}", normal_style))


    story.append(Spacer(1, 12))
    story.append(Paragraph("We are excited to welcome you to our institution.", normal_style))

    doc.build(story)
    return pdf_filename


@app.route('/admin/application/<int:application_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def view_application(application_id):
    if not isinstance(current_user, Admin):
        flash("You are not authorized to access this page", 'error')
        return redirect(url_for('index'))
        
    application = Application.query.get_or_404(application_id)
    form = AdminReviewForm()
    
    if form.validate_on_submit():
        selected_status = form.status.data
        if selected_status == 'Approved':
            pdf_filename = generate_admission_letter(application)
            application.pdf_path = f"admission_letter_{application.id}.pdf"
        application.status = selected_status
        db.session.commit()
        flash('Application updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('view_application.html', application=application, form=form)


@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'pdfs'), filename, as_attachment=True)



@app.route('/submit_application', methods=['POST'])
@login_required
def submit_application():
     form = ApplicationForm()
     if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone = form.phone.data
        degree = form.degree.data
        university = form.university.data
        id_proof = form.id_proof.data
        degree_certificate = form.degree_certificate.data

        id_proof_filename = None
        degree_certificate_filename = None

        # Handle file uploads
        if id_proof:
            if allowed_file(id_proof.filename):
                id_proof_filename = secure_filename(id_proof.filename)
                upload_path = os.path.join(app.root_path, 'static/uploads')
                os.makedirs(upload_path, exist_ok=True)
                id_proof.save(os.path.join(upload_path, id_proof_filename))
            else:
                flash("Invalid file format for ID Proof. Allowed formats: PDF, JPG, PNG, JPEG", 'error')
                return redirect(url_for('student_dashboard'))

        if degree_certificate:
            if allowed_file(degree_certificate.filename):
                degree_certificate_filename = secure_filename(degree_certificate.filename)
                upload_path = os.path.join(app.root_path, 'static/uploads')
                os.makedirs(upload_path, exist_ok=True)
                degree_certificate.save(os.path.join(upload_path, degree_certificate_filename))
            else:
                flash("Invalid file format for Degree Certificate. Allowed formats: PDF, JPG, PNG, JPEG", 'error')
                return redirect(url_for('student_dashboard'))

        new_application = Application(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            degree=degree,
            university=university,
            id_proof=id_proof_filename,
            degree_certificate=degree_certificate_filename,
        )
        if current_user.is_authenticated:
           new_application.user_id = current_user.id
        db.session.add(new_application)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('student_dashboard'))
     else:
       return redirect(url_for('student_dashboard'))



@app.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/uploads'), filename)

def create_folders():
    """Creates the necessary folders: instance, pdfs, and static/uploads."""

    # Create 'instance' folder
    instance_path = "instance"
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print(f"Created folder: {instance_path}")
    else:
         print(f"Folder already exists: {instance_path}")

    # Create 'pdfs' folder
    pdfs_path = "pdfs"
    if not os.path.exists(pdfs_path):
        os.makedirs(pdfs_path)
        print(f"Created folder: {pdfs_path}")
    else:
        print(f"Folder already exists: {pdfs_path}")


    # Create 'uploads' folder inside 'static'
    static_uploads_path = os.path.join("static", "uploads")

    if not os.path.exists("static"):
      os.makedirs("static")
      print("Created folder: static")
    else:
      print("Folder already exists: static")

    if not os.path.exists(static_uploads_path):
        os.makedirs(static_uploads_path)
        print(f"Created folder: {static_uploads_path}")
    else:
        print(f"Folder already exists: {static_uploads_path}")

if __name__ == '__main__':
    create_folders()
    app.run(debug=True)