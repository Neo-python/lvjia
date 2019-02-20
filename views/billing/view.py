from flask import render_template
from views.billing import billing
from models.common import Order
from plugins.common import Permission


@billing.route('/', methods=['GET'])
@Permission.need_login()
def index():
    """出单页面"""
    orders = Order.query.all()
    return render_template('billing/index.html', orders=orders)


@billing.route('/invoice/print/<int:order_id>', methods=['GET'])
@Permission.need_login()
def invoice_print(order_id):
    """发货单打印"""
    order = Order.query.get(order_id)
    price_sum = round(sum([form.price * form.quantity for form in order.forms]), 2)
    return render_template('billing/invoice_common.html', order=order, price_sum=price_sum)
