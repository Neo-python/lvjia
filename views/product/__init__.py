"""产品层"""
from flask import Blueprint

product = Blueprint('product', __name__, url_prefix='/product')
from views.product.view import *
