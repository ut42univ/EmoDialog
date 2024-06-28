import os
from controllers import DiaryController
from models import db, Diary
from flask import Flask
from flask import render_template, request, redirect, url_for
from sqlalchemy import desc
# from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary_app.db'
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)
with app.app_context():
    db.create_all()

# login_manager = LoginManager()
# login_manager.init_app(app)

id = 1

@app.route("/")
def indexPage():
    return render_template('index.html')

@app.route("/create_diary", methods=['GET', 'POST'])
def createDiaryPage():
    if request.method == 'GET':
        return render_template('create_diary.html')
    
    if request.method == 'POST':
        body = request.form['body']
        user_id = id
        diary = Diary(user_id, body)

        if len(body) == 0:
            return 'Body is empty'
        else:
            diary.create(body)
     
        return redirect(url_for('diariesPage'))

@app.route("/diaries")
def diariesPage():
    diaries = Diary.query.order_by(desc(Diary.create_at)).all()
    return render_template('diaries.html', diaries=diaries)

@app.route("/diaries/<int:diary_id>")
def diaryPage(diary_id):
    diary = DiaryController.query.get(diary_id)
    return render_template('diary.html', diary=diary)

@app.route("/diaries/<int:diary_id>/edit")
def editDiaryPage(diary_id):
    diary = DiaryC.query.get(diary_id)
    return render_template('edit_diary.html', diary=diary)

@app.route("/diaries/<int:diary_id>/update", methods=['POST'])
def updateDiary(diary_id):
    new_body = request.form['body']
    diary = Diary.query.get(diary_id)
    diary.edit(diary_id, new_body)
    return redirect(url_for('diariesPage'))

@app.route("/diaries/<int:diary_id>/delete")
def deleteDiary(diary_id):
    diary = Diary.query.get(diary_id)
    diary.delete(diary_id)
    return redirect(url_for('diariesPage'))

@app.route("/chat")
def chatPage():
    return render_template('chat.html')

@app.route("/analysis")
def analysisPage():
    return render_template('analysis.html')




if __name__ == ('__main__'):
    app.run(debug=True)