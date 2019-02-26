"""模板过滤器层"""
import datetime
from init import Redis
from flask import session, request
from plugins.common import OrdersInfo


class Name:
    """生产详情页,检测上下两个表单联系人是否相同,相同的情况下不再标注联系人姓名"""

    def __init__(self):
        """用法单一,无需设置参数"""
        self.name = ''

    def check(self, name: str) -> bool:
        """检测联系人
        :param name: order_form订单联系人信息
        """
        if self.name == name:
            return True
        else:
            self.name = name
            return False


def orders_info(orders: list) -> dict:
    """jinja模板直接调取多个order订单聚合数据"""
    return OrdersInfo(orders=orders).collect_quantity()


def real_status() -> bool:
    """验证实数权限状态
    将当前session记录的唯一session_id与redis缓存的唯一session_id进行匹配.
    """
    admin = session.get('admin')
    if admin:  # session过期时,直接返回False.不再读取redis.
        session_id = session.get('session_id')
        redis_token = Redis.get(f'real_admin_{admin.get("id")}')
        if redis_token == session_id:
            return True
    return False


def form_total_price(forms, real: bool = False) -> float:
    """多条表单总价计算
    计算多个order_form表单总价
    :param forms: 多条order_form
    :param real: False:form.quantity  True:form.real_quantity
    :return: 多条表单总价
    """
    price = 0.0
    for form in forms:
        if real:
            price += float(form.real_quantity * form.price)
        else:
            price += float(form.quantity * form.price)
    return price


def orders_total_price(orders, real: bool = False) -> bool:
    """多个订单总价
    :param orders: Order
    :param real: real: False:form.quantity  True:form.real_quantity
    :return: 多个订单总价
    """
    price = 0.0
    for order in orders:
        price += form_total_price(forms=order.forms, real=real)
    return price


def blueprint(aims: str) -> str:
    """判断当前蓝图与目标蓝图是否一致
    request.blueprint -> 当前蓝图名
    :param aims: 需要确认是否一致的蓝图名
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
    orders_total_price,
    Name
)


#  过滤器

def datetime_string(aims: datetime.datetime, fmt: str = '%Y-%m-%d %H:%M') -> str:
    """时间类型数据类型转换"""
    return aims.strftime(fmt)


filters = (
    datetime_string,
)
