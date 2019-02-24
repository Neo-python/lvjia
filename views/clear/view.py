"""结算层视图"""
from views.clear import clear
from flask import render_template, request
from models.common import Order, Firm, OrderForm
from plugins.common import OrdersInfo


@clear.route('/orders_info/', methods=['POST'])
def orders_info():
    """对账数据详情
    real -> Ture:使用real_quantity计算数据 False:使用order_form.quantity计算
    personnel -> 同一公司,不同联系人的数据统计计算 {联系人姓名:{'summary': 订单数汇总, forms: 归属于此联系人的订单详情[form1,form2]}}
    orders_info -> 公司数据汇总
    :return:
    """
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
