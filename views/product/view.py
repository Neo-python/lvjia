from flask import render_template, request, redirect, url_for
from views.product import product
from models.common import Product, Firm, ProductUnit
from plugins.common import page_generator


@product.route('/', methods=['GET'])
def index():
    """主页,列表页"""
    page = int(request.args.get('page', 1))
    products = Product.query.paginate(page=page, per_page=30)
    data = {
        'page': page_generator(page, max_num=products.pages, url=url_for('product.index')),
        'products': products.items
    }
    return render_template('product/index.html', **data)


@product.route('/unit/', methods=['GET'])
def unit_index():
    """产品单位首页"""
    return render_template('product/unit_index.html', unit_list=ProductUnit.basic_unit())


@product.route('/fixed_price/<int:company_id>/', methods=['GET'])
def fixed_price(company_id):
    """固定价格"""
    company = Firm.query.get(company_id)
    return render_template('product/fixed_price.html', company=company, unit_list=ProductUnit.basic_unit())


@product.route('/fixed_price/<int:company_id>/', methods=['POST'])
def fixed_price_post(company_id):
    """固定价格.表单提交
    """
    form = request.form.to_dict()
    form.pop('unit')
    unit_list = request.form.getlist('unit')

    firm = Firm.query.get(company_id)
    # 更新专价数据
    for i, ep in enumerate(firm.EP):
        ep.price = float(form[str(ep.id)])
        ep.unit_id = int(unit_list[i])
    firm.direct_update_()  # 保存操作
    return redirect(url_for('product.fixed_price', company_id=company_id))


@product.route('/new/', methods=['GET'])
def new():
    """新增产品页"""
    return render_template('product/new.html', unit_list=ProductUnit.basic_unit())


@product.route('/new/', methods=['POST'])
def new_post():
    """新增产品.表单提交
    新增产品数据提交后,broadcast函数为每家公司设定专价.
    """
    name = request.form.get('name')
    price = request.form.get('price')
    unit_id = request.form.get('unit_id')

    Product(name=name, price=price, unit_id=unit_id).direct_commit_().broadcast()

    return redirect(url_for('product.index'))


@product.route('/<int:product_id>/edit/', methods=['GET'])
def edit(product_id):
    """编辑产品"""
    return render_template('product/edit.html', product=Product.query.get(product_id),
                           unit_list=ProductUnit.basic_unit())


@product.route('/<int:product_id>/edit/', methods=['POST'])
def edit_post(product_id):
    """编辑产品.表单提交页"""
    product_ = Product.query.get(product_id)
    product_.name = request.form.get('name')
    product_.unit_id = request.form.get('unit_id')
    product_.price = request.form.get('price')
    product_.direct_update_()
    return redirect(url_for('product.index'))


@product.route('/<int:product_id>/delete/', methods=['GET'])
def delete(product_id):
    """删除产品"""
    Product.query.get(product_id).direct_delete_()
    return redirect(url_for('product.index'))


@product.route('/unit/new/', methods=['GET'])
def unit_new():
    """新建单位"""
    return render_template('product/unit_new.html')


@product.route('/unit/new/', methods=['POST'])
def unit_new_post():
    """新建单位.表单提交"""
    name = request.form.get('name')
    multiple = request.form.get('multiple')
    ProductUnit(name=name, multiple=multiple, parent=0).direct_commit_()
    return redirect(url_for('product.unit_index'))


@product.route('/unit/child/<int:unit_id>/', methods=['GET'])
def unit_child(unit_id):
    """设定子单位"""
    return render_template('product/unit_child.html', parent=ProductUnit.query.get(unit_id))


@product.route('/unit/child/<int:unit_id>/', methods=['POST'])
def unit_child_post(unit_id):
    """设定子单位.表单提交"""
    name = request.form.get('name')
    multiple = float(request.form.get('multiple'))

    ProductUnit(name=name, multiple=multiple, parent=unit_id).direct_commit_()
    return redirect(url_for('product.unit_index'))
