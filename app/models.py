from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os
from openai import OpenAI

client = OpenAI(
    
)



db = SQLAlchemy()

# Entity classes
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(120))
    diaries = db.relationship('Diary', backref='author', lazy=True)
    chats = db.relationship('Chat', backref='user', lazy=True)

class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(pytz.timezone('Asia/Tokyo'))
    )
    update_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(pytz.timezone('Asia/Tokyo')),
        onupdate=lambda: datetime.now(pytz.timezone('Asia/Tokyo'))
    )
    body = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(500))
    emotion = db.Column(db.String(100))
    emotion_degree = db.Column(db.Integer)
        

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(30), nullable=True)
    message = db.Column(db.Text, nullable=True)
    time = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Tokyo')))

class EmotionAI():
    def analyze_diary(self, body:str) -> tuple[str, str, int]:
        return f'Response for {body}!', 'happy', 90
    
    def generate_chat(self, messages:list[str]) -> str:
        prompt = '\n'.join(messages)
        return f'received {prompt}!'