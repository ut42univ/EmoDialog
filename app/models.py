from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask_login import UserMixin
from datetime import datetime
import pytz
from dotenv import load_dotenv
from openai import OpenAI
import json
import asyncio

load_dotenv()
db = SQLAlchemy()
client = OpenAI()

# Entity classes
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(120))

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
    message = db.Column(db.Text, nullable=True) # Text Type: unlimited length string (SQLAlchemy)
    time = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Tokyo')))

class EmotionAI():
    gpt_model = "gpt-3.5-turbo"
    num_messages = 4
    diary_role = "You are a psychology counselor. You are replying to the user's diary."
    chat_role = "You are a psychology counselor."
    analysis_role = """
        You are a psychology counselor designed to output JSON.
        You are analyzing the user's diary.
        
        Please analyze the user's diary and output the emotion and the degree of the emotion.
        The emotion is a string(neutral, happy, sad, angry, surprised, afraid).
        the degree of the emotion is an integer(0 to 100, 0 is a bad day, 100 is a very good day).
        
        example:
        {"emotion": strings, "emotion_degree": integer}
        """

    async def analyze_diary(self, body:str) -> tuple[str, str, int]:
        response_task = self.generate_diary_response(body)
        analysis_task = self.generate_analysis_response(body)

        response, (emotion, emotion_degree) = await asyncio.gather(response_task, analysis_task)
        
        return response, emotion, emotion_degree
    
    async def generate_diary_response(self, body:str) -> str:
        completion = client.chat.completions.create(
            model=self.gpt_model,
            messages=[
                {"role": "system", "content": self.diary_role},
                {"role": "user", "content": body}
            ]
        )
        return completion.choices[0].message.content

    async def generate_analysis_response(self, body:str) -> tuple[str, int]:
        completion = client.chat.completions.create(
            model=self.gpt_model,
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": self.analysis_role},
                {"role": "user", "content": body}
            ]
        )
        try:
            response = completion.choices[0].message.content
            dict_response = json.loads(response)
            emotion = dict_response['emotion']
            emotion_degree = dict_response['emotion_degree']
            return emotion, emotion_degree
        except:
            return 'neutral', 50
        
    def generate_chat_response(self, messages:list[str]) -> str:
        plain_messages = '\n'.join(messages[-self.num_messages:])
        completion = client.chat.completions.create(
            model=self.gpt_model,
            messages=[
                {"role": "system", "content": self.chat_role},
                {"role": "user", "content": plain_messages}
            ]
        )
        return completion.choices[0].message.content
