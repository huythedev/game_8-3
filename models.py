from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class StringEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_string = db.Column(db.String(500), nullable=False)
    transformed_string = db.Column(db.String(500), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    accessed = db.Column(db.Boolean, default=False)
    reaccesible = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    logged_in_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class StringPair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_pattern = db.Column(db.String(500), nullable=False, unique=True)
    output_pattern = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
