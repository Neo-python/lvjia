"""管理员层"""
from flask import Blueprint

admin = Blueprint('admin', __name__)
from views.admin.view import *
