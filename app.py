from flask import render_template
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

from plugins.filters import filter_funcs

for filter_ in filter_funcs:
    app.add_template_global(filter_, filter_.__name__)


@app.route('/', methods=['GET'])
def index():
    from flask import request
    n = request.args.getlist('name')
    return render_template('base.html')


if __name__ == '__main__':
    app.run()
