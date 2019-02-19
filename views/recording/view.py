import datetime
from flask import render_template, request, redirect, url_for, jsonify
from views.recording import recording
from models.common import Firm, Order, OrderForm


@recording.route('/index/', )
def index():
    """首页"""


@recording.route('/<int:company_id>/', methods=['GET'])
def recording_page(company_id):
    """录单页"""
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    return render_template('recording/recording.html', company=Firm.query.get(company_id), now=now)


@recording.route('/<int:company_id>/', methods=['POST'])
def recording_post(company_id):
    """录单.表单提交"""
    # 创建订单备注信息
    remarks = request.form.get('remarks')
    deadline = request.form.get('deadline')
    order = Order(company_id=company_id, remarks=remarks, deadline=deadline).direct_flush_()

    # 创建订单具体信息
    personnel_ = request.form.getlist('personnel')
    product_ = request.form.getlist('product_id')
    price_ = request.form.getlist('price')
    quantity_ = request.form.getlist('quantity')
    unit_ = request.form.getlist('unit')
    real_ = request.form.getlist('real')

    for person, product, price, quantity, unit, real in zip(personnel_, product_, price_, quantity_, unit_, real_):
        OrderForm(person_id=person, product_id=product, price=price, quantity=quantity,
                  order_id=order.id, unit_id=unit, real_quantity=real).direct_add_()
    order.direct_update_()  # 保存提交内容
    return redirect(url_for('billing.index'))


@recording.route('/edit/<int:order_id>/', methods=['GET'])
def order_edit(order_id):
    """订单修改"""
    order = Order.query.get(order_id)
    return render_template('recording/order_edit.html', order=order)


@recording.route('/edit/<int:order_id>/', methods=['POST'])
def order_edit_post(order_id):
    """订单修改.表单提交
    更新order信息
    收集表单数据
    更新order form 已存数据信息
    新增order form
    """

    # 更新order信息
    remarks = request.form.get('remarks')
    deadline = request.form.get('deadline')
    Order.query.filter_by(id=order_id).update({'remarks': remarks, 'deadline': deadline})

    # 收集表单数据
    ids = request.form.getlist('id')
    personnel_ = request.form.getlist('personnel')
    product_ = request.form.getlist('product_id')
    price_ = request.form.getlist('price')
    quantity_ = request.form.getlist('quantity')
    unit_ = request.form.getlist('unit')
    real_ = request.form.getlist('real')

    # 对齐数据
    for i, person, product, price, quantity, unit, real in zip(ids, personnel_, product_, price_, quantity_, unit_,
                                                               real_):
        if i:
            # 更新order form 已存数据信息
            OrderForm.query.filter_by(id=int(i)).update({
                'person_id': person,
                'product_id': product,
                'price': price,
                'quantity': quantity,
                'unit_id': unit,
                'real_quantity': real

            })
        else:
            # 新增order form
            OrderForm(person_id=person, product_id=product, price=price, quantity=quantity, order_id=order_id,
                      unit_id=unit, real_quantity=real).direct_add_()
    Order.static_commit_()
    return redirect(url_for('firm.index'))


@recording.route('/form/<int:form_id>/delete/', methods=['GET'])
def form_delete(form_id):
    """删除订单"""
    OrderForm.query.get(form_id).direct_delete_()
    return jsonify({'statusCode': 200})
