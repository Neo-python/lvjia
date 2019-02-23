"""模板过滤器层"""
from init import Redis
from flask import session, request
from plugins.common import OrdersInfo


def orders_info(orders: list) -> dict:
    """jinja模板函数"""
    return OrdersInfo(orders=orders).collect_quantity()


def real_status():
    """验证实数权限状态"""
    admin = session.get('admin')
    if admin:
        session_id = session.get('session_id')
        redis_token = Redis.get(f'real_admin_{admin.get("id")}')
        if redis_token == session_id:
            return True
    return False


def form_total_price(order, real: bool = False):
    """单项表单总价计算"""
    price = 0.0
    for form in order.forms:
        if real:
            price += float(form.real_quantity * form.price)
        else:
            price += float(form.quantity * form.price)
    return price


def orders_total_price(orders, real: bool = False):
    """订单集合总价"""
    price = 0.0
    for order in orders:
        price += form_total_price(order=order, real=real)
    return price


def blueprint(aims: str):
    """判断当前蓝图与目标蓝图是否一致
    :return: 'active' or ''
    """
    if request.blueprint == aims:
        return 'active'
    else:
        return ''


funcs = (
    orders_info,
    real_status,
    blueprint,
    form_total_price,
    orders_total_price
)
