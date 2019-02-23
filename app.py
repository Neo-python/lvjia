from flask import render_template, flash, redirect, url_for
from pymysql import install_as_MySQLdb
from init import create_app, db

install_as_MySQLdb()
app = create_app()
db.init_app(app=app)

from views.recording import recording
from views.firm import firm
from views.product import product
from views.billing import billing
from views.clear import clear
from views.admin import admin

app.register_blueprint(recording)
app.register_blueprint(firm)
app.register_blueprint(product)
app.register_blueprint(billing)
app.register_blueprint(clear)
app.register_blueprint(admin)

from plugins.filters import funcs

for func in funcs:
    app.add_template_global(func, func.__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('base.html')


@app.errorhandler(500)
def error500(err):
    """500错误"""
    flash(str(err), category='error')
    return redirect(url_for('index'))


@app.errorhandler(400)
def error400(err):
    """400错误"""
    flash(str(err), category='error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
