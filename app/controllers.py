from models import db, User, Diary, Chat, EmotionAI
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user


class UserController:
    def sign_up(self, username, password):
        user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()

    def login(self, username, password):
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return True
        return False
    
    def logout(self):
        logout_user()
    
    def user_load_control(self, user_id):
        return User.query.get(user_id)

class DiaryController:
    def create_diary(self, user_id:int, body:str):
        diary = Diary(user_id=user_id, body=body)
        db.session.add(diary)
        db.session.commit()

    def edit_diary(self, diary_id:int, new_body:str):
        diary = Diary.query.get(diary_id)
        if diary:
            diary.body = new_body
            db.session.commit()

    def delete_diary(self, diary_id):
        diary = Diary.query.get(diary_id)
        if diary:
            db.session.delete(diary)
            db.session.commit()

    def get_diary(self, diary_id):
        diary = Diary.query.get(diary_id)
        return diary
    
    def get_all(self):
        diaries = Diary.query.order_by(desc(Diary.create_at)).all()
        return diaries

class ChatController:
    def start_conversation(self, user_id):
        chat = Chat(user_id=user_id)
        db.session.add(chat)
        db.session.commit()

    def send_message(self, chat_id, message):
        chat = Chat.query.get(chat_id)
        if chat:
            chat.messages = (chat.messages or '') + f"\n{message}"
            db.session.commit()

    def delete_conversation(self, chat_id):
        chat = Chat.query.get(chat_id)
        if chat:
            db.session.delete(chat)
            db.session.commit()

class AnalysisController:
    def analyze_diary(self, diary_id):
        emotion_ai = EmotionAI(bot_name='Alice')
        response, emotion, degree = emotion_ai.analyze_emotion(diary_id)
        return response, emotion, degree
