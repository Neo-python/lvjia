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


def blueprint(aims: str):
    """判断当前蓝图与目标蓝图是否一致
    :return: 'active' or ''
    """
    if request.blueprint == aims:
        return 'active'
    else:
        return ''


filter_funcs = (
    orders_info,
    real_status,
    blueprint
)
