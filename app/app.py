import os
from controllers import UserController, DiaryController, ChatController, AnalysisController
from models import db, OperationalError
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask import render_template, request, redirect, url_for, abort, flash
from functools import wraps

from flask_login import LoginManager, login_required, current_user

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

# Controllers
userController = UserController()
diaryController = DiaryController()
chatController = ChatController()
analysisController = AnalysisController()

# Decorator for checking if the user is the owner of the diary
def diary_owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        diary_id = kwargs.get('diary_id', None)
        if not diaryController.is_diary_owner(diary_id, current_user.id):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return userController.user_load_control(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('loginPage'))

# Unauthenticated routes
@app.route("/login", methods=['GET', 'POST'])
def loginPage():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_success = userController.login(username, password)
        
        if not is_success:
            flash('認証失敗: Userが存在しないか、Passwordが間違っています。')
            return redirect(url_for('loginPage'))

        return redirect(url_for('indexPage'))

@app.route("/logout")
@login_required
def logout():
    flash(f'確認: ログアウトしました。')
    userController.logout()
    return redirect(url_for('loginPage'))
    
@app.route("/signup", methods=['GET', 'POST'])
def signUpPage():
    if request.method == 'GET':
        return render_template('sign_up.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_success = userController.sign_up(username, password)

        if not is_success:
            flash('エラー: このユーザー名はすでに使用されています。')
            return redirect(url_for('signUpPage'))

        flash('確認: ユーザー登録が完了しました。利用するにはログインしてください。')
        return redirect(url_for('loginPage'))

# Authenticated routes
@app.route("/")
@login_required
def indexPage():
    username = current_user.username
    return render_template('index.html', username=username)

# DiaryController
@app.route("/create_diary", methods=['GET', 'POST'])
@login_required
async def createDiaryPage():
    if request.method == 'GET':
        return render_template('create_diary.html')
    
    if request.method == 'POST':
        body = request.form['body']

        if len(body) == 0:
            return 'body needs strings.'
        else:    
            await diaryController.create_diary(current_user.id, body)
     
        return redirect(url_for('diariesPage'))

@app.route("/diaries")
@login_required
def diariesPage():
    diaries = diaryController.get_user_diaries(current_user.id)
    return render_template('diaries.html', diaries=diaries)

@app.route("/diaries/<int:diary_id>")
@login_required
@diary_owner_required
def diaryPage(diary_id):
    diary = diaryController.get_diary(diary_id)
    return render_template('diary.html', diary=diary)

@app.route("/diaries/<int:diary_id>/edit", methods=['GET', 'POST'])
@login_required
@diary_owner_required
def editDiaryPage(diary_id):
    if request.method == 'GET':
        diary = diaryController.get_diary(diary_id)
        return render_template('edit_diary.html', diary=diary)
    
    if request.method == 'POST':
        new_body = request.form['body']

        if len(new_body) == 0:
            return 'body needs strings.'
        else:
            diaryController.edit_diary(diary_id, new_body)
            return redirect(url_for('diariesPage'))

@app.route("/diaries/<int:diary_id>/delete")
@login_required
@diary_owner_required
def deleteDiary(diary_id):
    diaryController.delete_diary(diary_id)
    return redirect(url_for('diariesPage'))

# ChatController
@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chatPage():
    user_id = current_user.id
    if request.method == 'GET':
        chats = chatController.get_user_chat(user_id)
        return render_template('chat.html', user_id=user_id, chats=chats)
    
    if request.method == 'POST':
        message = request.form['message']
        chatController.send_message(user_id, message)
        return redirect(url_for('chatPage'))

@app.route("/chat/delete")
@login_required
def deleteChat():
    user_id = current_user.id
    chatController.delete_chat(user_id)
    return redirect(url_for('chatPage'))

# AnalysisController
@app.route("/analysis")
@login_required
async def analysisPage():
    user_id = current_user.id
    graph, pie = await analysisController.analysis_result(user_id)

    return render_template('analysis.html', graph=graph, pie=pie)


if __name__ == ('__main__'):
    app.run(debug=True)