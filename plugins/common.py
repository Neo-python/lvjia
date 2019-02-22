"""全局通用插件库"""
import datetime
from collections import Iterable
from functools import wraps
from flask import render_template, session, request, redirect, url_for, flash
from init import Redis


def page_generator(current_page_num: int, max_num: int, url: str, url_args: dict = None, style: str = 'action'):
    """分页生成器
    :param current_page_num: 当前页,页数
    :param max_num: 最大页数
    :param url: 分页地址,带问号.例:www.python.org/?
    :param url_args: 地址参数
    :param style:选中页样式.
    :return: 渲染后的分页html内容.
    """
    if not url_args:
        url_args = {}
    args = ''
    for k, v in url_args.items():
        args += f'&{k}={v}'
    page_info = {
        'max_num': max_num,
        'url': url,
        'url_args': args,
        'current_page_num': current_page_num,
        'action': style
    }
    return render_template('page.html', data=page_info)


class OrmVerity:

    @staticmethod
    def verify_deadline(deadline: str, fmt: str = '%Y-%m-%d %H:%M'):
        """验证期限"""
        if not deadline:
            return None
        try:
            _deadline = datetime.datetime.strptime(deadline, fmt)
        except Exception as err:
            print(err, '\n', deadline)
            return None
        else:
            return _deadline

    @staticmethod
    def verify_null_value(value, result=None):
        """验证空值,
        出现空值,返回预设结果或result默认值
        :param value: 验证值
        :param result: 结果
        :return: result
        """
        if not value:
            return result
        else:
            return value


class OrdersInfo:
    """订单信息集合"""

    def __init__(self, orders: list, real: bool = False):
        self.orders = orders if isinstance(orders, Iterable) else [orders]
        self.form_info = dict()
        self.real = real

    def collect_quantity(self) -> dict:
        """计算多个订单产品数量"""
        for order in self.orders:
            self.forms(order=order)
        return self.form_info

    def forms(self, order):
        """订单抽取单条表单"""
        if not self.real:
            for form in order.forms:
                self.update(form=form)
        else:
            for form in order.forms:
                self.real_update(form=form)

    def real_update(self, form):
        """更新实数"""
        multiple = form.unit.multiple / form.unit.parent_unit.multiple
        if self.form_info.get(form.product.name):
            """已有记录的产品"""
            # 订单记录数加上 --> 订单数量乘以订单所用单位倍数
            self.form_info[form.product.name]['quantity'] += form.real_quantity * multiple
        else:
            # 没有记录的产品
            self.form_info[form.product.name] = {
                'unit': form.unit.parent_unit.name,
                'quantity': form.real_quantity * multiple  # 订单数量乘以订单所用单位倍数
            }

    def update(self, form):
        """更新数据"""
        multiple = form.unit.multiple / form.unit.parent_unit.multiple
        if self.form_info.get(form.product.name):
            """已有记录的产品"""
            # 订单记录数加上 --> 订单数量乘以订单所用单位倍数
            self.form_info[form.product.name]['quantity'] += form.quantity * multiple
        else:
            # 没有记录的产品
            self.form_info[form.product.name] = {
                'unit': form.unit.parent_unit.name,
                'quantity': form.quantity * multiple  # 订单数量乘以订单所用单位倍数
            }


class Permission:
    """权限装饰器
    所有特殊条件验证函数,都需要设置默认值.
    """

    @staticmethod
    def need_login(level: int = 0):
        """需要登录
        :param level: 权限等级
        :return:视图函数或请求前url
        """

        def wrapper(func):
            @wraps(func)
            def inner(*args, **kwargs):

                login = Permission.verify_login()

                if not login:
                    return redirect(url_for('admin.login'))
                elif not Permission.need_login(level=level):
                    flash('权限不足,请切换到超级管理员账号!', category='error')
                    return redirect(request.headers.get('Referer'))
                else:
                    return func(*args, **kwargs)

            return inner

        return wrapper

    @staticmethod
    def verify_login() -> bool:
        """验证登录状态
        1.验证session状态
        2.通过redis验证登录状态是否过期
        3.验证登录状态是否属于当前session.
        4.验证失败后,清除session状态.再返回验证结果.
        :return: 验证结果与前台通知消息
        """
        admin = session.get('admin')
        session_id = session.get('session_id')
        if not admin:
            return False
        redis_token = Redis.get(f'admin_{admin.get("id")}')
        if redis_token:
            if redis_token == session_id:
                return True
            else:
                flash('您的账户已在异地登录,如果不是您本人操作,请联系管理员及时修改登录密码!', category='error')
        else:
            flash('登录状态已经过期,请重新登录', category='error')
        session.clear()  # 清除session状态
        return False

    @staticmethod
    def verify_level(level: int) -> bool:
        """验证权限等级"""
        admin = session.get('admin')
        if not Permission.verify_login():
            return False
        if admin['level'] >= level:
            return True
        else:
            return False
