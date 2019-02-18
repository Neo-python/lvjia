"""结算层视图"""
from views.clear import clear
from flask import render_template, redirect, url_for
from models.common import Order


@clear.route('/order/<int:order_id>/edit/', methods=['GET'])
def order_edit(order_id):
    """订单修改"""
    order = Order.query.get(order_id)
    return render_template('clear/../../templates/recording/order_edit.html', order=order)


@clear.route('/order/<int:order_id>/edit/', methods=['GET'])
def order_edit_post(order_id):
    """订单修改.表单提交"""
    return redirect(url_for('billing.index'))
