"""结算层"""
from flask import Blueprint

recording = Blueprint('clear', __name__)
from views.clear.view import *
