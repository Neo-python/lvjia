from flask import render_template
from app import app


@app.app_errorhandler(404)
def page_not_found(e):
    """404错误处理函数"""
    return render_template('404.html'), 404


@app.app_errorhandler(500)
def inter_server_error(e):
    """500系统内部错误处理函数"""
    return render_template('500.html'), 500
