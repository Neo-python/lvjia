"""结算层视图"""
from views.clear import clear
from flask import render_template, redirect, url_for
from models.common import Order


@clear.route('/order/<int:order_id>/edit/', methods=['GET'])
def order_edit(order_id):
    """订单修改"""
    order = Order.query.get(order_id)

