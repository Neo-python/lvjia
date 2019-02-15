from flask import render_template
from views.recording import recording


@recording.route('/index/', )
def index():
    """首页"""



@recording.route('/', methods=['GET'])
def recording_page():
    """录单页"""
    return render_template('recording/recording.html')
