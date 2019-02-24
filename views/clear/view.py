"""结算层视图"""
from views.clear import clear
from flask import render_template, request
from models.common import Order, Firm, OrderForm
from plugins.common import OrdersInfo


@clear.route('/orders_info/', methods=['POST'])
def orders_info():
    """订单详情"""
    firm = Firm.query.get(request.form.get('firm_id'))
    order_ids = request.form.getlist('order_ids')
    if request.args.get('model', None) == 'real':
        real = True
    else:
        real = False

    personnel = dict()
    for person in firm.personnel:
        forms = person.forms.filter(OrderForm.order_id.in_(order_ids)).all()
        person_form_info = OrdersInfo(forms=forms, real=real).collect_forms()
        personnel.update({person.name: {'summary': person_form_info, 'forms': forms}})

    orders = Order.query.filter(Order.id.in_(order_ids)).all()
    orders_info_ = OrdersInfo(orders=orders, real=real).collect_quantity()
    return render_template('clear/orders_info.html', orders=orders, orders_info=orders_info_, real=real, firm=firm,
                           person_forms=personnel)
