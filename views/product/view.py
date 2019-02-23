from flask import render_template, request, redirect, url_for, flash
from views.product import product
from models.common import Product, Firm, ProductUnit
from plugins.common import page_generator, Permission


@product.route('/', methods=['GET'])
@Permission.need_login()
def index():
    """主页,列表页"""
    page = int(request.args.get('page', 1))
    products = Product.query.paginate(page=page, per_page=10)
    data = {
        'page': page_generator(page, max_num=products.pages, url=url_for('product.index')),
        'products': products.items
    }
    return render_template('product/index.html', **data)


@product.route('/unit/', methods=['GET'])
@Permission.need_login()
def unit_index():
    """产品单位首页"""
    return render_template('product/unit_index.html')


@product.route('/fixed_price/<int:firm_id>/', methods=['GET'])
@Permission.need_login()
def fixed_price(firm_id):
    """固定价格"""
    firm = Firm.query.get(firm_id)
    return render_template('product/fixed_price.html', firm=firm)


@product.route('/fixed_price/<int:firm_id>/', methods=['POST'])
@Permission.need_login()
def fixed_price_post(firm_id):
    """固定价格.表单提交
    """
    form = request.form.to_dict()

    firm = Firm.query.get(firm_id)
    # 更新专价数据
    for i, ep in enumerate(firm.EP):
        ep.price = float(form[str(ep.id)])
    firm.direct_update_()  # 保存操作
    return redirect(url_for('product.fixed_price', firm_id=firm_id))


@product.route('/new/', methods=['GET'])
@Permission.need_login()
def new():
    """新增产品页"""
    return render_template('product/new.html')


@product.route('/new/', methods=['POST'])
@Permission.need_login()
def new_post():
    """新增产品.表单提交
    新增产品数据提交后,broadcast函数为每家公司设定专价.
    """
    name = request.form.get('name')

    return redirect(url_for('product.edit', product_id=Product(name=name).direct_commit_().id))


@product.route('/<int:product_id>/edit/', methods=['GET'])
@Permission.need_login()
def edit(product_id):
    """编辑产品"""
    return render_template('product/edit.html', product=Product.query.get(product_id))


@product.route('/<int:product_id>/edit/', methods=['POST'])
@Permission.need_login()
def edit_post(product_id):
    """编辑产品.表单提交页"""
    product_ = Product.query.get(product_id)
    product_.name = request.form.get('name')
    product_.direct_update_()
    return redirect(url_for('product.index'))


@product.route('/<int:product_id>/delete/', methods=['GET'])
@Permission.need_login(level=1)
def delete(product_id):
    """删除产品"""
    Product.query.get(product_id).direct_delete_()
    return redirect(url_for('product.index'))


@product.route('/<int:product_id>/unit/new/', methods=['GET'])
@Permission.need_login()
def unit_new(product_id):
    """新建单位"""
    product_ = Product.query.get(product_id)
    return render_template('product/unit_new.html', product=product_)


@product.route('/<int:product_id>/unit/new/', methods=['POST'])
@Permission.need_login()
def unit_new_post(product_id):
    """新建单位.表单提交"""
    try:
        name = request.form.get('name')
        price = request.form.get('price')
        multiple = request.form.get('multiple', 1)
        parent_id = request.form.get('parent_id', 0)
        unit = ProductUnit(name=name, multiple=multiple, parent_id=parent_id, product_id=product_id, price=price)
        unit.direct_commit_()
    except BaseException as err:
        flash(str(err), category='error')
        flash('操作失败!请检查是否存在重复单位名', category='error')
    else:
        unit.broadcast()
    return redirect(url_for('product.edit', product_id=product_id))


@product.route('/unit/<int:unit_id>/edit/', methods=['GET'])
def unit_edit(unit_id):
    """编辑单位"""
    unit = ProductUnit.query.get(unit_id)
    return render_template('product/unit_edit.html', unit=unit)


@product.route('/unit/<int:unit_id>/edit/', methods=['POST'])
def unit_edit_post(unit_id):
    """编辑单位 表单提交"""
    # 表单获取
    unit_name = request.form.get('name')
    unit_multiple = request.form.get('multiple')
    price = request.form.get('price')
    # 更新数据
    unit = ProductUnit.query.get(unit_id)
    unit.name = unit_name
    unit.multiple = unit_multiple
    unit.price = price
    unit.direct_update_()

    return redirect(url_for('product.edit', product_id=unit.product_id))
