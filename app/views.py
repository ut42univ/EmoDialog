# views.py
from flask.views import MethodView
from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from functools import wraps
import asyncio
from controllers import UserController, DiaryController, ChatController, AnalysisController

# Initialize controllers
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

class LoginView(MethodView):
    def get(self) -> str:
        return render_template('login.html')

    def post(self) -> str:
        username = request.form['username']
        password = request.form['password']
        is_success = userController.login(username, password)

        if not is_success:
            flash('認証失敗: Userが存在しないか、Passwordが間違っています。')
            return redirect(url_for('loginPage'))

        return redirect(url_for('indexPage'))

class LogoutView(MethodView):
    @login_required
    def get(self) -> str:
        flash(f'確認: ログアウトしました。')
        userController.logout()
        return redirect(url_for('loginPage'))

class SignUpView(MethodView):
    def get(self)  -> str:
        return render_template('sign_up.html')

    def post(self) -> str:
        username = request.form['username']
        password = request.form['password']
        is_success = userController.sign_up(username, password)

        if not is_success:
            flash('エラー: このユーザー名はすでに使用されているか、ユーザー名またはパスワードが空です。')
            return redirect(url_for('signUpPage'))

        flash('確認: ユーザー登録が完了しました。利用するにはログインしてください。')
        return redirect(url_for('loginPage'))

class IndexView(MethodView):
    @login_required
    def get(self) -> str:
        username = current_user.username
        return render_template('index.html', username=username)

class CreateDiaryView(MethodView):
    @login_required
    def get(self) -> str:
        return render_template('create_diary.html')
    
    @login_required
    def post(self) -> str:
        body = request.form['body']
        is_success = asyncio.run(diaryController.create_diary(current_user.id, body))

        if not is_success:
            flash('エラー: 日記本文は1字以上500文字以内で入力してください。')
            return render_template('create_diary.html', body=body)
        flash('確認: 日記を作成しました。')
        return redirect(url_for('diariesPage'))

class EditDiaryView(MethodView):
    @login_required
    @diary_owner_required
    def get(self, diary_id:int) -> str:
        diary = diaryController.get_diary(diary_id)
        body = diary.body
        return render_template('edit_diary.html', body=body)
    
    @login_required
    @diary_owner_required
    def post(self, diary_id:int) -> str:
        new_body = request.form['body']
        is_success = asyncio.run(diaryController.edit_diary(diary_id, new_body))

        if not is_success:
            flash('エラー: 日記本文は1字以上500文字以内で入力してください。')
            return render_template('edit_diary.html', body=new_body)
        flash(f'確認: 日記を編集しました。（日記ID: {diary_id}）')
        return redirect(url_for('diariesPage'))

class DiariesView(MethodView):
    @login_required
    def get(self) -> str:
        diaries = diaryController.get_user_diaries(current_user.id)
        if not diaries:
            flash('警告: 日記が記録されていません。')
        return render_template('diaries.html', diaries=diaries)

class DiaryView(MethodView):
    @login_required
    @diary_owner_required
    def get(self, diary_id:int) -> str:
        diary = diaryController.get_diary(diary_id)
        return render_template('diary.html', diary=diary)

class DeleteDiaryView(MethodView):
    @login_required
    @diary_owner_required
    def get(self, diary_id:int) -> str:
        diaryController.delete_diary(diary_id)
        flash(f'確認: 日記を削除しました。（日記ID: {diary_id}）')
        return redirect(url_for('diariesPage'))

class ChatView(MethodView):
    @login_required
    def get(self) -> str:
        user_id = current_user.id
        chats = chatController.get_user_chat(user_id)
        return render_template('chat.html', user_id=user_id, chats=chats)
    
    @login_required
    def post(self) -> str:
        user_id = current_user.id
        message = request.form['message']
        is_success = chatController.send_message(user_id, message)

        if not is_success:
            flash('エラー: メッセージは1字以上200文字以内で入力してください。')
        return redirect(url_for('chatPage'))

class DeleteChatView(MethodView):
    @login_required
    def get(self) -> str:
        user_id = current_user.id
        chatController.delete_chat(user_id)
        flash('確認: チャットを削除しました。')
        return redirect(url_for('chatPage'))

class AnalysisView(MethodView):
    @login_required
    def get(self) -> str:
        user_id = current_user.id
        diaries = diaryController.get_user_diaries(user_id)

        if not diaries:
            flash('警告: 日記が記録されていないため、感情分析結果を表示できません。')

        graph, pie = asyncio.run(analysisController.analysis_result(user_id))

        return render_template('analysis.html', graph=graph, pie=pie)
