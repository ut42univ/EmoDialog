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
    max_body_length = 500

    def create_diary(self, user_id:int, body:str):
        diary = Diary(user_id=user_id, body=body)
        db.session.add(diary)
        db.session.commit()

        diary_id = diary.id
        AnalysisController().analyze_diary(diary_id)

    def edit_diary(self, diary_id:int, new_body:str):
        diary = Diary.query.get(diary_id)
        if diary:
            diary.body = new_body
            db.session.commit()

            diary_id = diary.id
            AnalysisController().analyze_diary(diary_id)

    def delete_diary(self, diary_id):
        diary = Diary.query.get(diary_id)
        if diary:
            db.session.delete(diary)
            db.session.commit()

    def is_diary_owner(self, diary_id, user_id):
        diary = Diary.query.get(diary_id)
        try:
            if diary.user_id == user_id:
                return True
        except:
            return False
        return False

    def get_diary(self, diary_id):
        diary = Diary.query.get(diary_id)
        return diary
    
    def get_user_diaries(self, user_id: int):
        diaries = Diary.query.order_by(desc(Diary.create_at)).filter_by(user_id=user_id).all()
        return diaries
    
    def get_all_diaries(self):
        diaries = Diary.query.order_by(desc(Diary.create_at)).all()
        return diaries

class ChatController:

    def send_message(self, user_id, message):
        chat = Chat(user_id=user_id, message=message, role='user')
        db.session.add(chat)
        db.session.commit()

        chats = self.get_user_chat(user_id)
        messages = [chat.message for chat in chats]
        response = EmotionAI().generate_chat(messages)

        chat_response = Chat(user_id=user_id, message=response, role='assistant')
        db.session.add(chat_response)
        db.session.commit()

    def get_user_chat(self, user_id) -> list:
        chats = Chat.query.filter_by(user_id=user_id).all()
        return chats

    def delete_chat(self, user_id):
        chats = Chat.query.filter_by(user_id=user_id).all()
        if chats:
            for chat in chats:
                db.session.delete(chat)
                db.session.commit()

class AnalysisController:
    def analyze_diary(self, diary_id):
        emotion_ai = EmotionAI()
        diary = Diary.query.get(diary_id)
        response, emotion, degree = emotion_ai.analyze_diary(diary.body)
        diary.response = response
        diary.emotion = emotion
        diary.emotion_degree = degree
        db.session.commit()