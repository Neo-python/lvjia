"""结算层视图"""
from views.clear import clear
from flask import render_template, request
from models.common import Order
from plugins.common import OrdersInfo


@clear.route('/orders_info/', methods=['POST'])
def orders_info():
    """订单详情"""
    if request.args.get('model', None) == 'real':
        real = True
    else:
        real = False

    order_ids = request.form.getlist('order_ids')
    orders = Order.query.filter(Order.id.in_(order_ids)).all()
    form_info = OrdersInfo(orders=orders, real=real).collect_quantity()
    return render_template('clear/form_info.html', orders=orders, form_info=form_info, real=real)
