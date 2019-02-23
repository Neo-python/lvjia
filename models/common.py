"""通用模型模块"""
from sqlalchemy import or_
from models import db, Common
from plugins.common import OrmVerity


class Firm(Common, db.Model):
    """公司模型"""
    __tablename__ = 'firm'
    id = db.Column(db.Integer, index=True, primary_key=True)

    name = db.Column(db.String(length=50), nullable=False, unique=True, comment='公司/单位名')
    address = db.Column(db.String(length=255), default='', comment='公司/单位地址')

    personnel = db.relationship('People', lazy='select', cascade="all, delete-orphan", backref='firm')
    EP = db.relationship('ExternalPrice', lazy='dynamic', cascade="all, delete-orphan", backref='firm')
    orders = db.relationship('Order', lazy='select', cascade="all, delete-orphan", backref='firm')

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

    def init_external_price(self):
        """初始化所有产品的公司专价,只允许在新建公司时执行一次"""
        for product in Product.query.all():
            for unit in product.units:
                ExternalPrice(product.id, self.id, unit.price, unit.id).direct_add_()
        return self.direct_commit_()

    @property
    def ep_all(self):
        """返回公司专价"""
        return self.EP.all()

    @property
    def product_data(self):
        """得到所有产品数据"""
        result = dict()
        for i in self.EP:
            if result.get(i.product_id):
                result[i.product_id]['units'].update({i.unit_id: {'name': i.unit.name, 'price': float(i.price)}})

            else:
                result[i.product_id] = {'name': i.product.name,
                                        'units': {i.unit_id: {'name': i.unit.name, 'price': float(i.price)}}}
        return result


class Product(Common, db.Model):
    """产品模型"""
    __tablename__ = 'product'
    id = db.Column(db.Integer, index=True, primary_key=True)

    name = db.Column(db.String(length=50), nullable=False, comment='产品名')

    units = db.relationship('ProductUnit', lazy='select', backref='product')

    def __init__(self, name: str):
        self.name = name

    @property
    def unit_all(self):
        """可用计量单位"""
        return ProductUnit.query.filter(or_(ProductUnit.product_id == self.id)).all()


class ProductUnit(Common, db.Model):
    """产品单位"""
    __tablename__ = 'product_unit'
    id = db.Column(db.Integer, index=True, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, comment='产品单位')
    name = db.Column(db.String(length=50), nullable=False, comment='单位名')
    price = db.Column(db.DECIMAL(9, 2), default=0, nullable=False, comment='价格')
    multiple = db.Column(db.DECIMAL(precision=9, decimal_return_scale=2), default=1, nullable=False, comment='与父级单位倍率')
    parent_id = db.Column(db.SMALLINT, db.ForeignKey('product_unit.id'), default=0, nullable=False,
                          comment='单位等级,0:基础单位,其他:父级单位.')

    subordinates = db.relationship('ProductUnit', lazy='select')

    def __init__(self, product_id, name: str, price: float, multiple: float, parent_id: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.multiple = multiple
        self.parent_id = parent_id

    def broadcast(self):
        """新建产品完成后,只允许执行一次.将数据更新每家公司的专价
        broadcast:广播
        """
        for firm in Firm.query.all():
            ExternalPrice(self.product_id, firm.id, self.price, self.id).direct_commit_()

    @property
    def parent(self):
        """上级对象"""
        if getattr(self, '_parent', None) or self.parent_id is not 0:
            # 查询到上级对象时,缓存上级对象
            self._parent = ProductUnit.query.get(self.parent_id)
            return self._parent
        else:
            return None

    @property
    def parent_unit(self):
        """父级单位"""
        if self.parent:
            return self.parent
        else:
            return self


class People(Common, db.Model):
    """人员模型"""
    __tablename__ = 'people'
    id = db.Column(db.Integer, index=True, primary_key=True)

    name = db.Column(db.String(length=50), nullable=False, comment='人名')
    telephone = db.Column(db.String(length=13), default='', nullable=False, comment='联系方式')
    firm_id = db.Column(db.Integer, db.ForeignKey('firm.id'), nullable=False)
    remarks = db.Column(db.String(length=255), default='', comment='人员备注')

    order_form_all = db.relationship('OrderForm', lazy='select', backref='person')

    def __init__(self, name: str, telephone: str, firm_id: int, remarks: str = None):
        self.name = name
        self.telephone = telephone
        self.firm_id = firm_id
        self.remarks = remarks


class ExternalPrice(Common, db.Model):
    """公司/单位专价模型"""
    __tablename__ = 'external_price'
    id = db.Column(db.Integer, index=True, primary_key=True)

    firm_id = db.Column(db.Integer, db.ForeignKey('firm.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.DECIMAL(precision=9, decimal_return_scale=2), default=0.00, nullable=False, comment='产品单价')
    unit_id = db.Column(db.SMALLINT, db.ForeignKey('product_unit.id'), nullable=False, comment='产品单位ID')

    unit = db.relationship('ProductUnit', lazy='select')
    product = db.relationship('Product', lazy='select')

    def __init__(self, product_id: int, firm_id: int, price: float, unit_id: int):
        self.product_id = product_id
        self.firm_id = firm_id
        self.price = price
        self.unit_id = unit_id


class OrderForm(Common, db.Model):
    """订单模型"""
    __tablename__ = 'order_form'
    id = db.Column(db.Integer, index=True, primary_key=True)

    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False, comment='订单目标对象')
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, comment='产品编号')
    price = db.Column(db.DECIMAL(precision=9, decimal_return_scale=2), default=0.0, comment='订单价格')
    quantity = db.Column(db.DECIMAL(precision=9, decimal_return_scale=2), default=0.0, comment='订单数量')
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, comment='订单备注编号')
    unit_id = db.Column(db.SMALLINT, db.ForeignKey('product_unit.id'), nullable=False, comment='产品单位ID')
    real_quantity = db.Column(db.DECIMAL(9, 2), nullable=False, comment='实际发货数量')

    unit = db.relationship('ProductUnit', lazy='select')
    product = db.relationship('Product', lazy='select')

    def __init__(self, person_id: int, product_id: int, price: float, quantity: float, order_id: int, unit_id: int,
                 real_quantity: float = None):
        self.person_id = person_id
        self.product_id = product_id
        self.price = price
        self.quantity = quantity
        self.order_id = order_id
        self.unit_id = unit_id
        self.real_quantity = self._init_real_quantity(real_quantity)

    def _init_real_quantity(self, quantity):
        """实际数量初始化设定"""
        try:
            quantity = float(quantity)
        except TypeError:
            return self.quantity
        except ValueError:
            return self.quantity
        else:
            return quantity


class Order(Common, db.Model):
    """订单备注信息模型"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, index=True, primary_key=True)

    firm_id = db.Column(db.Integer, db.ForeignKey('firm.id'), nullable=False, comment='公司编号')
    remarks = db.Column(db.String(length=255), default='', nullable=False, comment='订单备注')
    datetime = db.Column(db.TIMESTAMP, name='datetime', nullable=False, comment='订单创建日期')
    deadline = db.Column(db.Date, comment='订单期限')

    forms = db.relationship('OrderForm', lazy='select', cascade="all, delete-orphan", backref='order')

    def __init__(self, firm_id: int, remarks: str, deadline=None):
        self.firm_id = firm_id
        self.remarks = OrmVerity.verify_null_value(value=remarks, result=None)
        self.deadline = OrmVerity.verify_deadline(deadline=deadline)

    def peoples_info(self):
        """获取订单联系人集合"""
        result = dict()
        for form in self.forms:
            result[form.person.name] = {'telephone': form.person.telephone, 'remarks': form.person.remarks}
        return result

    @property
    def deadline_to_string(self):
        """期限字符串格式化"""
        if self.deadline:
            if self.deadline.hour < 1:
                return self.deadline.strftime('%Y-%m-%d')
            else:
                return self.deadline.strftime('%Y-%m-%d %H:%M')
        else:
            return ''

    @property
    def deadline_to_weekday(self):
        """获取期限星期几"""
        week_map = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '日'}
        if self.deadline:
            return f'星期{week_map[self.deadline.weekday() + 1]}'
        else:
            return ''

    @property
    def string_deadline(self):
        """时间格式化"""
        return f'{self.deadline_to_string}  {self.deadline_to_weekday}'

    def deadline_format(self, fmt: str, week: bool):
        """期限自定义格式化"""
        if not self.deadline:
            return self.datetime.strftime(fmt)

        string = self.deadline.strftime(fmt)
        if week:
            return f'{string} {self.deadline_to_weekday}'
        else:
            return string
