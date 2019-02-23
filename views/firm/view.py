import datetime
from flask import render_template, request, redirect, url_for
from plugins.common import page_generator, Permission
from views.firm import firm
from models.common import Firm, People, Order


@firm.route('/', methods=['GET'])
@Permission.need_login()
def index():
    """主页,列表页"""
    firms = Firm.query.all()
    return render_template('firm/index.html', firms=firms)


@firm.route('/new/', methods=['GET'])
@Permission.need_login()
def new():
    """新增公司/单位"""
    return render_template('firm/new.html')


@firm.route('/new/', methods=['POST'])
@Permission.need_login()
def new_post():
    """新增公司/单位,表单提交"""
    name = request.form.get('name')
    address = request.form.get('address')

    new_company = Firm(name=name, address=address).direct_commit_().init_external_price()
    return redirect(url_for('firm.people_new', firm_id=new_company.id))


@firm.route('/<int:firm_id>/index/', methods=['GET'])
@Permission.need_login()
def company_index(firm_id):
    """公司主页"""
    firm_ = Firm.query.get(firm_id)
    page = int(request.args.get('page', 1))
    orders = Order.query.filter_by(firm_id=firm_id).order_by(Order.id).paginate(page=page, per_page=30)
    data = {
        'orders': orders.items,
        'page': page_generator(page, max_num=orders.pages, url=url_for('firm.company_index', firm_id=firm_id))
    }
    return render_template('firm/firm_index.html', firm=firm_, **data)


@firm.route('/<int:firm_id>/edit/', methods=['GET'])
@Permission.need_login()
def company_edit(firm_id):
    """公司信息编辑页"""
    firm_ = Firm.query.get(firm_id)
    return render_template('firm/edit.html', firm=firm_)


@firm.route('/<int:firm_id>/edit/', methods=['POST'])
@Permission.need_login()
def company_edit_post(firm_id):
    """公司信息编辑表单提交"""
    company = Firm.query.get(firm_id)
    company.name = request.form.get('name')
    company.address = request.form.get('address')

    company.direct_update_()
    return redirect(url_for('firm.company_index', firm_id=firm_id))


@firm.route('/people/new/<int:firm_id>', methods=['GET'])
@Permission.need_login()
def people_new(firm_id):
    """新建联系人"""
    return render_template('firm/new_people.html', firm_id=firm_id)


@firm.route('/people/new/', methods=['POST'])
@Permission.need_login()
def people_new_post():
    """新建联系人表单提交"""
    firm_id = request.form.get('firm_id')
    name = request.form.get('name')
    telephone = request.form.get('telephone')
    remarks = request.form.get('remarks')

    People(firm_id=firm_id, name=name, telephone=telephone, remarks=remarks).direct_commit_()
    return redirect(url_for('firm.company_index', firm_id=firm_id))


@firm.route('/people/<int:people_id>/edit/', methods=['GET'])
@Permission.need_login()
def people_edit(people_id):
    """人员信息修改页"""
    people = People.query.get(people_id)
    return render_template('firm/edit_people.html', people=people)


@firm.route('/people/<int:people_id>/edit/', methods=['POST'])
@Permission.need_login()
def people_edit_post(people_id):
    """人员信息编辑,表单提交"""
    people = People.query.get(people_id)
    name = request.form.get('name')
    telephone = request.form.get('telephone')
    remarks = request.form.get('remarks')
    people.name = name
    people.telephone = telephone
    people.remarks = remarks
    people.direct_update_()
    return redirect(url_for('firm.company_index', firm_id=people.firm_id))


@firm.route('/people/<int:people_id>/delete/', methods=['GET'])
@Permission.need_login(level=1)
def people_delete(people_id):
    """人员删除"""
    people = People.query.get(people_id).direct_delete_()
    return redirect(url_for('firm.company_index', firm_id=people.firm_id))


@firm.route('/<int:firm_id>/order_list/', methods=['GET'])
@Permission.need_login()
def order_list(firm_id):
    """公司订单列表
    page:页码
    per_page:每页数据条数
    start:起始时间
    end:结束时间
    query:orm查询对象
    orders:sqlalchemy分页器
    data:模板渲染内置参数
        page:分页栏 type -> html_string
        args:搜索条件表单参数
    :param firm_id: 公司编号
    """

    # 收集表单参数
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 0))
    if per_page == 0:
        per_page = Order.query.filter_by(firm_id=firm_id).count()

    start = request.args.get('start')
    end = request.args.get('end')

    # 选择查询条件
    query = Order.query.filter_by(firm_id=firm_id).order_by(Order.id.desc())
    if start:
        query = query.filter(Order.datetime > datetime.datetime.strptime(start, '%Y-%m-%d'))
    if end:
        query = query.filter(Order.datetime < datetime.datetime.strptime(end, '%Y-%m-%d'))

    # 聚合数据,渲染模板.
    orders = query.paginate(page=page, per_page=per_page)
    data = {
        'firm_id': firm_id,
        'orders': orders.items,
        'page': page_generator(page, max_num=orders.pages, url=url_for('firm.order_list', firm_id=firm_id)),
        'args': request.args.to_dict()
    }
    return render_template('firm/order_list.html', **data)
