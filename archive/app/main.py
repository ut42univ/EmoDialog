from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
# run when you want to create a database
# with app.app_context():
#     db.create_all()

class Diary(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
    )
    name = db.Column(
        db.String(80), 
        nullable=False
    )
    body = db.Column(
        db.String(255), 
        nullable=False
    )
    reply = db.Column(
        db.String(255), 
        nullable=True
    )
    emotion = db.Column(
        db.String(255), 
        nullable=True
    )
    created_at = db.Column(
        db.DateTime, 
        nullable=False, 
        default=lambda: datetime.now(pytz.timezone('Asia/Tokyo'))
    )
    updated_at = db.Column(
        db.DateTime, 
        nullable=False, 
        default=lambda: datetime.now(pytz.timezone('Asia/Tokyo')), 
        onupdate=lambda: datetime.now(pytz.timezone('Asia/Tokyo'))
    )

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/create_diary", methods=['GET', 'POST'])
def createDiary():
    if request.method == 'GET':
        return render_template('createDiary.html')
    
    if request.method == 'POST':
        body = request.form['body']

        new_diary = Diary(    
            name = 'user_name',
            body = body
        )
        db.session.add(new_diary)
        db.session.commit()

        return redirect(url_for('index'))

@app.route("/diaries")
def viewDiaries():
    diaries = Diary.query.order_by(desc(Diary.created_at)).all()
    return render_template('viewDiaries.html', diaries=diaries)

@app.route("/diaries/<int:id>")
def viewDiary(id):
    # diary = Daily.query.get(id)
    return render_template('diary.html', id=id)

@app.route("/diaries/<int:id>/edit")
def editDiary(id):
    diary = Diary.query.get(id)
    return render_template('editDiary.html', diary=diary)

@app.route("/diaries/<int:id>/update", methods=['POST'])
def updateDiary(id):
    diary = Diary.query.get(id)
    diary.body = request.form['body']
    db.session.commit()
    return redirect(url_for('viewDiaries'))

@app.route("/diaries/<int:id>/delete")
def deleteDiary(id):
    diary = Diary.query.get(id)
    db.session.delete(diary)
    db.session.commit()
    return redirect(url_for('viewDiaries'))

@app.route("/chat")
def chatWithAI():
    return render_template('chatWithAI.html')

@app.route("/view_analysis")
def viewAnalysis():
    # diaries = Daily.query.all()
    return render_template('viewAnalysis.html')


if __name__ == ('__main__'):
    app.run(debug=True)