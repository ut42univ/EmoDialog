from flask import Flask
# from models import db
from flask import render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary_app.db'


# db.init_app(app)

# with app.app_context():
#     db.create_all()

@app.route("/")
def indexPage():
    return render_template('index.html')

@app.route("/create_diary")
def createDiaryPage():
    return render_template('create_diary.html')

@app.route("/diaries")
def diariesPage():
    return render_template('diaries.html')

@app.route("/diaries/<int:diary_id>")
def diaryPage(diary_id):
    return render_template('diary.html', diary_id=diary_id)

@app.route("/diaries/<int:diary_id>/edit")
def editDiaryPage(diary_id):
    return render_template('edit_diary.html', diary_id=diary_id)

@app.route("/diaries/<int:diary_id>/delete")
def deleteDiaryPage(diary_id):
    return 'Deleted diary with id: ' + str(diary_id)

@app.route("/chat")
def chatPage():
    return render_template('chat.html')

@app.route("/analysis")
def analysisPage():
    return render_template('analysis.html')




if __name__ == ('__main__'):
    app.run(debug=True)