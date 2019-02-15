from flask import render_template
from views.company import company


@company.route('/', methods=['GET'])
def index():
    """主页,列表页"""
    return render_template('company/index.html')
