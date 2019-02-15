from flask import render_template
from views.product import product


@product.route('/', methods=['GET'])
def index():
    """主页,列表页"""
    return render_template('product/index.html')
