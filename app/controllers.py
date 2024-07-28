from models import db, User, Diary, Chat, EmotionAI
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
import matplotlib
import matplotlib.pyplot as plt 
from io import BytesIO
import base64
import asyncio

class UserController:
    def sign_up(self, username:str, password:str) -> bool:

        # Check enmpy username and password
        if not username or not password:
            return False
        
        # create a new user and add it to the database if the username is unique
        try:
            user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(user)
            db.session.commit()
            return True
        except:
            return False

    def login(self, username:str, password:str) -> bool:
        
        # Check if the user exists
        # Check if the password is correct
        try:
            user = User.query.filter_by(username=username).first()
            if check_password_hash(user.password, password):
                login_user(user)
                return True
            else:
                # password is incorrect
                return False
        except:
            # user does not exist
            return False

    
    def logout(self) -> None:
        logout_user()
    
    def user_load_control(self, user_id:int) -> User:
        return User.query.get(user_id)

class DiaryController:
    max_body_length = 500

    def __init__(self) -> None:
        self.analysisController = AnalysisController()

    async def create_diary(self, user_id:int, body:str) -> bool:
        is_valid = self.check_body_length(body)

        if not is_valid:
            return False
        
        diary = Diary(user_id=user_id, body=body)
        db.session.add(diary)
        db.session.commit()

        diary_id = diary.id
        await self.analysisController.analyze_diary(diary_id)

        # return True if the diary is created successfully
        return True

    async def edit_diary(self, diary_id:int, new_body:str) -> bool:
        is_valid = self.check_body_length(new_body)

        if not is_valid:
            return False
        
        diary = Diary.query.get(diary_id)
        if diary:
            diary.body = new_body
            db.session.commit()

            diary_id = diary.id
            await self.analysisController.analyze_diary(diary_id)

            # return True if the diary is edited successfully
            return True
        else:
            return False

    def delete_diary(self, diary_id:int) -> None:
        diary = Diary.query.get(diary_id)
        if diary:
            db.session.delete(diary)
            db.session.commit()

    def is_diary_owner(self, diary_id:int, user_id:int) -> bool:
        diary = Diary.query.get(diary_id)
        try:
            if diary.user_id == user_id:
                return True
        except:
            return False
        return False
    
    def check_body_length(self, body:str) -> bool:
        if len(body) > self.max_body_length:
            return False
        elif len(body) == 0:
            return False
        return True

    def get_diary(self, diary_id:int) -> Diary:
        diary = Diary.query.get(diary_id)
        return diary
    
    def get_user_diaries(self, user_id:int) -> list:
        diaries = Diary.query.order_by(desc(Diary.create_at)).filter_by(user_id=user_id).all()
        return diaries
    
    def get_all_diaries(self) -> list:
        diaries = Diary.query.order_by(desc(Diary.create_at)).all()
        return diaries

class ChatController:
    max_message_length = 200

    def __init__(self) -> None:
        self.emotion_ai = EmotionAI()

    def send_message(self, user_id:int, message:str) -> bool:

        if not message:
            return False
        elif len(message) > self.max_message_length:
            return False
        
        chat = Chat(user_id=user_id, message=message, role='user')
        db.session.add(chat)
        db.session.commit()

        chats = self.get_user_chat(user_id)
        messages = [chat.message for chat in chats]
        response = self.emotion_ai.generate_chat_response(messages)

        chat_response = Chat(user_id=user_id, message=response, role='assistant')
        db.session.add(chat_response)
        db.session.commit()

        # return True if the message is sent successfully
        return True

    def get_user_chat(self, user_id:int) -> list:
        chats = Chat.query.filter_by(user_id=user_id).all()
        return chats

    def delete_chat(self, user_id:int) -> None:
        chats = Chat.query.filter_by(user_id=user_id).all()
        if chats:
            for chat in chats:
                db.session.delete(chat)
                db.session.commit()

class AnalysisController:

    def __init__(self) -> None:
        self.emotion_ai = EmotionAI()

    async def analyze_diary(self, diary_id:int) -> None:
        diary = Diary.query.get(diary_id)
        response, emotion, degree = await self.emotion_ai.analyze_diary(diary.body)
        diary.response = response
        diary.emotion = emotion
        diary.emotion_degree = degree
        db.session.commit()

    async def analysis_result(self, user_id:int) -> tuple[str, str]:

        async def create_graph():
            # create graph
            fig_1 = plt.figure(figsize=(16, 9), dpi=300)
            ax_1 = fig_1.add_subplot(1,1,1)
            ax_1.set_ylim(0, 100)
            ax_1.plot(range(len(create_at)), emotion_degree, color='indigo', linestyle='--', linewidth=2.0, marker='o')
            ax_1.set_xlabel("Create At")
            ax_1.set_ylabel("Emotion Degree")
            ax_1.fill_between(range(len(create_at)), emotion_degree, 17, color='indigo', alpha=0.3)
            ax_1.set_xticks(range(len(create_at)))
            ax_1.set_xticklabels(create_at)
            for x, y, emotion in zip(range(len(create_at)), emotion_degree, emotions):
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

            return base64_image_graph
        
        async def create_pie_chart():
            # create pie chart
            emotions_list = list(set(emotions))
            emotions_size = [emotions.count(emotion) for emotion in emotions_list]

            cmap=plt.get_cmap("tab20b")
            colors = [cmap(i) for i in range(len(emotions_size))]

            plt.rcParams['font.size'] = 16.0

            fig_2 = plt.figure(figsize=(16, 9) ,dpi=300)
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

            return base64_image_pie
        
        diaries = Diary.query.filter_by(user_id=user_id).all()
        create_at = [diary.create_at.strftime('%m/%d %H:%M') for diary in diaries]
        emotions = [diary.emotion for diary in diaries]
        emotion_degree = [diary.emotion_degree for diary in diaries]

        matplotlib.use('Agg')
        plt.style.use('ggplot')

        create_graph_task = create_graph()
        create_pie_chart_task = create_pie_chart()

        base64_image_graph, base64_image_pie = await asyncio.gather(create_graph_task, create_pie_chart_task)

        return base64_image_graph, base64_image_pie