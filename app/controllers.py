from models import db, User, Diary, Chat, EmotionAI
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
import matplotlib
import matplotlib.pyplot as plt 
from io import BytesIO
import base64

class UserController:
    def sign_up(self, username, password):
        user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()

    def login(self, username, password):
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        try:
            if check_password_hash(user.password, password):
                login_user(user)
                return True
        except:
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
        response = EmotionAI().generate_chat_response(messages)

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

    def analysis_result(self, user_id):
        diaries = Diary.query.filter_by(user_id=user_id).all()
        create_at = [diary.create_at.strftime('%m/%d %H:%M') for diary in diaries]
        emotions = [diary.emotion for diary in diaries]
        emotion_degree = [diary.emotion_degree for diary in diaries]

        matplotlib.use('Agg')
        plt.style.use('ggplot')

        # create graph
        fig_1 = plt.figure(figsize=(15, 5))
        ax_1 = fig_1.add_subplot(1,1,1)
        ax_1.set_ylim(0, 100)
        ax_1.plot(create_at, emotion_degree, color='indigo',  linestyle='--', linewidth = 2.0, marker='o') 
        ax_1.set_xlabel("Create At")
        ax_1.set_ylabel("Emotion Degree")
        ax_1.fill_between(create_at, emotion_degree, 17, color='indigo', alpha=0.3)
        for x, y, emotion in zip(create_at, emotion_degree, emotions):
            ax_1.text(x, y+2, emotion, color="dimgray")    
        ax_1.tick_params(labelbottom=True, labelleft=False)
        ax_1.tick_params(bottom=False, left=False)
        plt.box(False)
        
        io_1 = BytesIO()
        fig_1.savefig(io_1, format='png')
        io_1.seek(0)
        base64_image_graph = base64.b64encode(io_1.read()).decode()
        plt.clf()
        plt.close(fig_1)
        io_1.close()

        # create pie chart
        emotions_list = list(set(emotions))
        emotions_size = [emotions.count(emotion) for emotion in emotions_list]

        cmap=plt.get_cmap("tab20b")
        colors = [cmap(i) for i in range(len(emotions_size))]

        fig_2 = plt.figure(figsize=(15, 5))
        ax_2 = fig_2.add_subplot(1,1,1)
        ax_2.pie(emotions_size, labels=emotions_list, autopct='%1.1f%%', startangle=90, colors=colors)
        ax_2.axis('equal')
        plt.box(False)

        io_2 = BytesIO()
        fig_2.savefig(io_2, format='png')
        io_2.seek(0)
        base64_image_pie = base64.b64encode(io_2.read()).decode()
        plt.clf()
        plt.close(fig_2)
        io_2.close()

        return base64_image_graph, base64_image_pie