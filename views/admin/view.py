import datetime
from flask import render_template, redirect, url_for, request, flash, session
from views.admin import admin
from models.admin import Admin
from plugins.common import Permission
from app import app


@admin.route('/login/', methods=['GET'])
def login():
    """登录页面"""
    if session.get('admin'):
        return 'ok'
    return render_template('admin/login.html')


@admin.route('/login/', methods=['POST'])
def login_post():
    """登录页表单提交"""
    account = request.form.get('account')
    password = request.form.get('password')
    remember = request.form.get('remember')
    check_result = Admin.login(account=account, password=password)
    if not check_result:
        flash(message='账户或密码错误', category='error')
        return redirect(url_for('admin.login'))

    session['admin'] = check_result.to_dict_()
    if remember:
        session_deadline = datetime.timedelta(days=7)
    else:
        session_deadline = datetime.timedelta(hours=3)
    app.permanent_session_lifetime = session_deadline
    return redirect(url_for('index'))


@admin.route('/logout/', methods=['GET'])
@Permission.need_login()
def logout():
    """登出操作"""
    session.clear()
    return redirect(url_for('admin.login'))
