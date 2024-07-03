from flask import Blueprint, render_template, request
from controllers import AnalysisController

analysis_blueprint = Blueprint('analysis', __name__)

@analysis_blueprint.route('/analysis', methods=['GET', 'POST'])
def analyze_diary():
    if request.method == 'POST':
        diary_id = request.form['diary_id']
        analysis_controller = AnalysisController()
        response, emotion, degree = analysis_controller.analyze_diary(diary_id)
        return render_template('analysis_result.html', response=response, emotion=emotion, degree=degree)
    return render_template('analysis.html')
