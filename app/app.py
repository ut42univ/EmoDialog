# app.py
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
import os
from views import (
    LoginView, LogoutView, SignUpView, IndexView, CreateDiaryView, 
    EditDiaryView, DiariesView, DiaryView, DeleteDiaryView, 
    ChatView, DeleteChatView, AnalysisView
)
from models import User, db
from sqlalchemy.exc import OperationalError

# initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample_app.db'
app.config['SECRET_KEY'] = os.urandom(24)

bootstrap = Bootstrap5(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginPage'

db.init_app(app)
with app.app_context():
    try:
        db.create_all()
    except OperationalError:
        pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# URL routes
app.add_url_rule('/login', view_func=LoginView.as_view('loginPage'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
app.add_url_rule('/signup', view_func=SignUpView.as_view('signUpPage'))
app.add_url_rule('/', view_func=IndexView.as_view('indexPage'))
app.add_url_rule('/create_diary', view_func=CreateDiaryView.as_view('createDiaryPage'))
app.add_url_rule('/diaries/<int:diary_id>/edit', view_func=EditDiaryView.as_view('editDiaryPage'))
app.add_url_rule('/diaries', view_func=DiariesView.as_view('diariesPage'))
app.add_url_rule('/diaries/<int:diary_id>', view_func=DiaryView.as_view('diaryPage'))
app.add_url_rule('/diaries/<int:diary_id>/delete', view_func=DeleteDiaryView.as_view('deleteDiary'))
app.add_url_rule('/chat', view_func=ChatView.as_view('chatPage'))
app.add_url_rule('/chat/delete', view_func=DeleteChatView.as_view('deleteChat'))
app.add_url_rule('/analysis', view_func=AnalysisView.as_view('analysisPage'))

if __name__ == '__main__':
    app.run(debug=True)
