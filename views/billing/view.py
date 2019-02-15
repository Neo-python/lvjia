from flask import render_template
from views.billing import billing


@billing.route('/', methods=['GET'])
def index():
    """出单页面"""
    return render_template('billing/index.html')
