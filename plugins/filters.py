"""模板过滤器层"""
from init import Redis
from flask import session
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


filter_funcs = (
    orders_info,
    real_status,
)
