"""结算层"""
from flask import Blueprint

clear = Blueprint('clear', __name__)
from views.clear.view import *
