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
    return redirect(url_for('firm.people_new', company_id=new_company.id))


@firm.route('/<int:company_id>/index/', methods=['GET'])
@Permission.need_login()
def company_index(company_id):
    """公司主页"""
    company = Firm.query.get(company_id)
    page = int(request.args.get('page', 1))
    orders = Order.query.filter_by(company_id=company_id).order_by(Order.id).paginate(page=page, per_page=30)
    data = {
        'orders': orders.items,
        'page': page_generator(page, max_num=orders.pages, url=url_for('firm.company_index', company_id=company_id))
    }
    return render_template('firm/firm_index.html', company=company, **data)


@firm.route('/<int:company_id>/edit/', methods=['GET'])
@Permission.need_login()
def company_edit(company_id):
    """公司信息编辑页"""
    company = Firm.query.get(company_id)
    return render_template('firm/edit.html', company=company)


@firm.route('/<int:company_id>/edit/', methods=['POST'])
@Permission.need_login()
def company_edit_post(company_id):
    """公司信息编辑表单提交"""
    company = Firm.query.get(company_id)
    company.name = request.form.get('name')
    company.address = request.form.get('address')

    company.direct_update_()
    return redirect(url_for('firm.company_index', company_id=company_id))


@firm.route('/people/new/<int:company_id>', methods=['GET'])
@Permission.need_login()
def people_new(company_id):
    """新建联系人"""
    return render_template('firm/new_people.html', company_id=company_id)


@firm.route('/people/new/', methods=['POST'])
@Permission.need_login()
def people_new_post():
    """新建联系人表单提交"""
    company_id = request.form.get('company_id')
    name = request.form.get('name')
    telephone = request.form.get('telephone')
    remarks = request.form.get('remarks')

    People(company_id=company_id, name=name, telephone=telephone, remarks=remarks).direct_commit_()
    return redirect(url_for('firm.company_index', company_id=company_id))


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
    return redirect(url_for('firm.company_index', company_id=people.company_id))


@firm.route('/people/<int:people_id>/delete/', methods=['GET'])
@Permission.need_login(level=1)
def people_delete(people_id):
    """人员删除"""
    people = People.query.get(people_id).direct_delete_()
    return redirect(url_for('firm.company_index', company_id=people.company_id))


@firm.route('/<int:company_id>/order_list/', methods=['GET'])
def order_list(company_id):
    """公司订单列表"""
    page = int(request.args.get('page', 1))
    orders = Order.query.filter_by(company_id=company_id).order_by(Order.id).paginate(page=page, per_page=10)
    data = {
        'company_id': company_id,
        'orders': orders.items,
        'page': page_generator(page, max_num=orders.pages, url=url_for('firm.order_list', company_id=company_id))
    }
    return render_template('firm/order_list.html', **data)
