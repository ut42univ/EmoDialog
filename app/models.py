from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz

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
    start_time = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Tokyo')))
    end_time = db.Column(db.DateTime)
    messages = db.Column(db.Text, nullable=True)

    def __init__(self, user_id:int):
        self.user_id = user_id

    def add_message(self, id:int, message:str):
        chat = Chat.query.filter_by(id=id).first()
        chat.messages += f'\n{message}'
        db.session.commit()
    
    def get_messages(self, id:int):
        chat = Chat.query.filter_by(id=id).first()
        return chat.messages

    def delete(self, id:int):
        chat = Chat.query.filter_by(id=id).first()
        db.session.delete(chat)
        db.session.commit()

class EmotionAI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bot_name = db.Column(db.String(100), nullable=False)

    def __init__(self, bot_name:str):
        self.bot_name = bot_name

    
    
    def analyze_emotion(self, diaryId:int):
        diary = Diary.query.filter_by(id=diaryId).first()
        body = diary.body
        
        return 'Response', 'Emotion', 90