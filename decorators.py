from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt, get_jwt_identity
from models import Admin, Student
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not isinstance(current_user, Admin):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not isinstance(current_user, Student):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function