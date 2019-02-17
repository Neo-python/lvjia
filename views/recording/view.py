import datetime
from flask import render_template, request, redirect, url_for
from views.recording import recording
from models.common import Firm, OrderRemarks, OrderForm


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
    order_remarks = OrderRemarks(company_id=company_id, remarks=remarks, deadline=deadline).direct_flush_()

    # 创建订单具体信息
    personnel_list = request.form.getlist('personnel')
    product_id_list = request.form.getlist('product_id')
    price_list = request.form.getlist('price')
    quantity_list = request.form.getlist('quantity')
    unit_list = request.form.getlist('unit')

    for person_id, product_id, price, quantity, unit_id in zip(personnel_list, product_id_list, price_list,
                                                               quantity_list, unit_list):

        OrderForm(person_id=person_id, product_id=product_id, price=price, quantity=quantity,
                  remarks_id=order_remarks.id, unit_id=unit_id).direct_add_()
    order_remarks.direct_update_()  # 保存提交内容
    return redirect(url_for('billing.index'))
