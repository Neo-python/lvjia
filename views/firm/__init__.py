"""公司与单位层"""
from flask import Blueprint

firm = Blueprint('firm', __name__, url_prefix='/firm')
from views.firm.view import *
