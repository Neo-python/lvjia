"""录单层"""
from flask import Blueprint

recording = Blueprint('recording', __name__, url_prefix='/recording')
from views.recording.view import *
