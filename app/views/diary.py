from flask import Blueprint, render_template, request, redirect, url_for
from controllers import DiaryController

diary_blueprint = Blueprint('diary', __name__)

@diary_blueprint.route('/diaries')
def diaries():
    # ユーザーの日記を取得して表示
    diaries = Diary.query.all()
    return render_template('diaries.html', diaries=diaries)

@diary_blueprint.route('/diary/create', methods=['GET', 'POST'])
def create_diary():
    if request.method == 'POST':
        body = request.form['body']
        user_id = 1  # 仮のユーザーID、実際には認証情報から取得
        diary_controller = DiaryController()
        diary_controller.create_diary(user_id, body)
        return redirect(url_for('diary.diaries'))
    return render_template('create_diary.html')

@diary_blueprint.route('/diary/edit/<int:diary_id>', methods=['GET', 'POST'])
def edit_diary(diary_id):
    if request.method == 'POST':
        new_body = request.form['body']
        diary_controller = DiaryController()
        diary_controller.edit_diary(diary_id, new_body)
        return redirect(url_for('diary.diaries'))
    return render_template('edit_diary.html', diary_id=diary_id)
