"""公司与单位层"""
from flask import Blueprint

company = Blueprint('company', __name__, url_prefix='/company')
from views.company.view import *
