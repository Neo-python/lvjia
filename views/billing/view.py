from flask import render_template, request, url_for
from sqlalchemy.sql.functions import count
from views.billing import billing
from models.common import Order
from plugins.common import Permission, page_generator, OrdersInfo


@billing.route('/', methods=['GET'])
@Permission.need_login()
def index():
    """出单页面"""
    page = int(request.args.get('page', 1))
    orders = Order.query.order_by(Order.id.desc()).paginate(page=page, per_page=10)
    data = {
        'orders': orders.items,
        'page': page_generator(page, max_num=orders.pages, url=url_for('billing.index'))
    }
    return render_template('billing/index.html', **data)


@billing.route('/invoice/print/<int:order_id>', methods=['GET'])
@Permission.need_login()
def invoice_print(order_id):
    """发货单打印"""
    order = Order.query.get(order_id)
    price_sum = round(sum([form.price * form.quantity for form in order.forms]), 2)
    return render_template('billing/invoice_common.html', order=order, price_sum=price_sum)


@billing.route('/orders_info/', methods=['GET'])
def orders_info():
    """订单信息汇总报表打印"""
    order_ids = request.args.getlist('order_id')
    orders = Order.query.filter(Order.id.in_(order_ids)).all()
    sort = [(len(order_.forms), order_) for order_ in orders]
    sort.sort(key=lambda x: x[0], reverse=True)
    orders = [item[1] for item in sort]
    form_info = OrdersInfo(orders=orders, real=True).collect_quantity()
    return render_template('billing/orders_info.html', orders=orders, form_info=form_info)
