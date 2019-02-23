import random, hashlib
from flask import render_template, redirect, url_for, request, flash, session
from views.admin import admin
from models.admin import Admin
from plugins.common import Permission
from init import Redis


@admin.route('/login/', methods=['GET'])
def login():
    """登录页面"""
    if Permission.verify_login():
        return redirect(url_for('index'))
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
    session['session_id'] = str(random.random())
    if remember:
        Redis.set(f'admin_{check_result.id}', value=session['session_id'], ex=60 * 60 * 24 * 7)
    else:
        Redis.set(f'admin_{check_result.id}', value=session['session_id'], ex=60 * 60 * 3)

    return redirect(url_for('index'))


@admin.route('/query/', methods=['POST'])
@Permission.need_login()
def real_status():
    """获取设置订单实数权限的视图函数
    :return: 回到主页
    """
    token = request.form.get('query')
    session_token = session['admin']['token']

    if Admin.verify_token(token=token, self_token=session_token):
        session_admin = session.get('admin')
        session_id = session.get('session_id')
        Redis.set(name=f'real_admin_{session_admin.get("id")}', value=session_id, ex=60 * 5)
    else:
        flash(message='Bad request', category='error')
    return redirect(url_for('index'))


@admin.route('/logout/', methods=['GET'])
@Permission.need_login()
def logout():
    """登出操作"""
    session.clear()
    return redirect(url_for('admin.login'))
