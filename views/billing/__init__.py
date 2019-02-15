"""出单层"""
from flask import Blueprint

billing = Blueprint('billing', __name__, url_prefix='/billing')
from views.billing.view import *
