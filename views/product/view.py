from flask import render_template, request, redirect, url_for
from views.product import product
from models.common import Product, Firm, ExternalPrice, ProductUnit
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
    return render_template('product/unit_index.html', unit_list=ProductUnit.query.all())


@product.route('/fixed_price/<int:company_id>/', methods=['GET'])
def fixed_price(company_id):
    """固定价格"""
    company = Firm.query.get(company_id)
    return render_template('product/fixed_price.html', company=company, unit_list=ProductUnit.query.all())


@product.route('/fixed_price/<int:company_id>/', methods=['POST'])
def fixed_price_post(company_id):
    """固定价格.表单提交
    unit_list 获得顺序与页面排列顺序一致, 专价更新后需要与form保持同步.
    """
    form = request.form.to_dict()
    form.pop('unit')
    unit_list = request.form.getlist('unit')
    firm = Firm.query.get(company_id)
    # 更新专价数据
    for i, ep in enumerate(firm.EP):
        product_id = str(ep.product_id)
        ep.price = float(form[product_id])
        ep.unit_id = int(unit_list[i])
        form.pop(product_id)  # 弹出已经操作的数据
        unit_list.pop(i)  # unit_list需要保持同步

    # 新建所有新产品专价
    for i, (product_id, price) in enumerate(form.items()):
        product_id = int(product_id)
        price = float(price)
        unit_id = int(unit_list[i])
        ExternalPrice(product_id=product_id, company_id=company_id, price=price, unit_id=unit_id).direct_commit_()
    firm.direct_update_()  # 保存操作
    return redirect(url_for('product.fixed_price', company_id=company_id))


@product.route('/new/', methods=['GET'])
def new():
    """新增产品页"""
    return render_template('product/new.html', unit_list=ProductUnit.query.all())


@product.route('/new/', methods=['POST'])
def new_post():
    """新增产品.表单提交"""
    name = request.form.get('name')
    price = request.form.get('price')
    unit_id = request.form.get('unit_id')

    Product(name=name, price=price, unit_id=unit_id).direct_commit_()
    return redirect(url_for('product.index'))


@product.route('/<int:product_id>/edit/', methods=['GET'])
def edit(product_id):
    """编辑产品"""
    return render_template('product/edit.html', product=Product.query.get(product_id),
                           unit_list=ProductUnit.query.all())


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
    ProductUnit(name=name, multiple=multiple).direct_commit_()
    return redirect(url_for('product.unit_index'))
