from flask_sqlalchemy import SQLAlchemy
# Importações atualizadas para compatibilidade com Flask 3.x
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    cpf = db.Column(db.String(14), unique=True, nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    profile = db.relationship('Profile', backref='user', uselist=False)
    documents = db.relationship('Document', backref='user', lazy=True)
    social_accounts = db.relationship('SocialAccount', backref='user', lazy=True)
    esports_profiles = db.relationship('EsportsProfile', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    interests = db.Column(db.Text)
    fan_story = db.Column(db.Text)
    favorite_games = db.Column(db.Text)
    other_games = db.Column(db.Text)
    favorite_teams = db.Column(db.Text)
    other_teams = db.Column(db.Text)
    events_attended = db.Column(db.Text)
    other_events = db.Column(db.Text)
    purchases = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(255))
    doc_type = db.Column(db.String(50))  # RG, CPF, comprovante de residência, etc.
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    verified = db.Column(db.Boolean, default=False)
    verification_date = db.Column(db.DateTime)

class SocialAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    platform = db.Column(db.String(50))  # Facebook, Twitter, Instagram, etc.
    account_id = db.Column(db.String(255))
    username = db.Column(db.String(100))
    access_token = db.Column(db.Text)
    token_expiry = db.Column(db.DateTime)
    last_sync = db.Column(db.DateTime)

class EsportsProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    platform = db.Column(db.String(50))  # Steam, Battlenet, Twitch, etc.
    profile_url = db.Column(db.String(255))
    username = db.Column(db.String(100))
    verified = db.Column(db.Boolean, default=False)
    relevance_score = db.Column(db.Float, default=0.0)  # Score calculado pelo AI
    verified_date = db.Column(db.DateTime)