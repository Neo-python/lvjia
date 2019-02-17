"""通用模型模块"""
from init import db
from plugins.common import OrmVerity


class Common(object):
    """orm通用操作"""

    def direct_flush_(self):
        """直接预提交"""
        self.direct_add_()
        self.flush_()
        return self

    def flush_(self):
        """预提交，等于提交到数据库内存，还未写入数据库文件"""
        db.session.flush()
        return self

    def direct_add_(self):
        """直接添加事务"""
        db.session.add(self)
        return self

    def direct_commit_(self):
        """直接提交"""
        self.direct_add_()
        db.session.commit()
        return self

    def direct_update_(self):
        """直接更新"""
        db.session.commit()
        return self

    def direct_delete_(self):
        """直接删除"""
        db.session.delete(self)
        db.session.commit()

    def __str__(self):
        return f'<class \'{self.__class__.__name__}\' id={self.id if self.id else None}>'

    def __repr__(self):
        """想要此特殊方法被模型继承,需要将Common继承顺序排在ORM基类之前"""
        description = ', '.join([f'{column.name}={getattr(self, column.key)}' for column in self.__table__._columns])
        return f'<{description}>'


class Firm(Common, db.Model):
    """公司模型"""
    __tablename__ = 'firm'
    id = db.Column(db.Integer, index=True, primary_key=True)

    name = db.Column(db.String(length=50), nullable=False, unique=True, comment='公司/单位名')
    address = db.Column(db.String(length=255), comment='公司/单位地址')

    personnel = db.relationship('People', lazy='select', cascade="all, delete-orphan", backref='firm')

    EP = db.relationship('ExternalPrice', lazy='select', cascade="all, delete-orphan", backref='firm')

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

    @property
    def products(self):
        """产品价格,固定价格将会覆盖原价"""
        products = Product.query.all()
        ep = self.EP
        prices = dict()
        for i in products:
            prices.update({i.id: {'name': i.name, 'unit_id': i.unit_id, 'unit_name': i.unit.name, 'price': i.price}})
        for i in ep:
            prices[i.product_id]['price'] = i.price
            prices[i.product_id]['unit_id'] = i.unit_id
        return prices


class Product(Common, db.Model):
    """产品模型"""
    __tablename__ = 'product'
    id = db.Column(db.Integer, index=True, primary_key=True)

    name = db.Column(db.String(length=50), nullable=False, comment='产品名')
    price = db.Column(db.Float(precision=9, decimal_return_scale=2), default=0.00, nullable=False, comment='产品单价')
    unit_id = db.Column(db.SMALLINT, db.ForeignKey('product_unit.id'), nullable=False, comment='产品单位ID')

    EPS = db.relationship('ExternalPrice', lazy='select', cascade="all, delete-orphan", backref='product')
    all_order = db.relationship('OrderForm', lazy='select', cascade="all, delete-orphan", backref='product')
    unit = db.relationship('ProductUnit', lazy='select')

    def __init__(self, name: str, price: float, unit_id: int = None):
        self.name = name
        self.price = price
        self.unit_id = unit_id


class ProductUnit(Common, db.Model):
    """产品单位"""
    __tablename__ = 'product_unit'
    id = db.Column(db.Integer, index=True, primary_key=True)

    name = db.Column(db.String(length=50), nullable=False, comment='产品名')
    multiple = db.Column(db.Integer, default=1, nullable=False, comment='最小单位的倍数')

    def __init__(self, name: str, multiple: int):
        self.name = name
        self.multiple = multiple


class People(Common, db.Model):
    """人员模型"""
    __tablename__ = 'people'
    id = db.Column(db.Integer, index=True, primary_key=True)

    name = db.Column(db.String(length=50), nullable=False, comment='人名')
    telephone = db.Column(db.String(length=13), nullable=False, comment='联系方式')
    company_id = db.Column(db.Integer, db.ForeignKey('firm.id'), nullable=False)
    remarks = db.Column(db.String(length=255), default='', comment='人员备注')

    def __init__(self, name: str, telephone: str, company_id: int, remarks: str = None):
        self.name = name
        self.telephone = telephone
        self.company_id = company_id
        self.remarks = remarks


class ExternalPrice(Common, db.Model):
    """公司/单位专价模型"""
    __tablename__ = 'external_price'
    id = db.Column(db.Integer, index=True, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('firm.id'), nullable=False)
    price = db.Column(db.Float(precision=9, decimal_return_scale=2), default=0.00, nullable=False, comment='产品单价')
    unit_id = db.Column(db.SMALLINT, db.ForeignKey('product_unit.id'), nullable=False, comment='产品单位ID')
    unit = db.relationship('ProductUnit', lazy='select')

    def __init__(self, product_id: int, company_id: int, price: float, unit_id: int):
        self.product_id = product_id
        self.company_id = company_id
        self.price = price
        self.unit_id = unit_id


class OrderForm(Common, db.Model):
    """订单模型"""
    __tablename__ = 'order_form'
    id = db.Column(db.Integer, index=True, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, comment='产品编号')
    price = db.Column(db.Float(precision=9, decimal_return_scale=2), default=0.0, comment='订单价格')
    quantity = db.Column(db.Float(precision=9, decimal_return_scale=2), default=0.0, comment='订单数量')
    remarks_id = db.Column(db.Integer, db.ForeignKey('order_remarks.id'), nullable=False, comment='订单备注编号')
    unit_id = db.Column(db.SMALLINT, nullable=False, comment='产品单位ID')

    def __init__(self, product_id: int, price: float, quantity: float, remarks_id: int, unit_id: int):
        self.product_id = product_id
        self.price = price
        self.quantity = quantity
        self.remarks_id = remarks_id
        self.unit_id = unit_id


class OrderRemarks(Common, db.Model):
    """订单备注信息模型"""
    __tablename__ = 'order_remarks'
    id = db.Column(db.Integer, index=True, primary_key=True)

    company_id = db.Column(db.Integer, nullable=False, comment='公司编号')
    remarks = db.Column(db.String(length=255), default='', nullable=False, comment='订单备注')
    datetime_ = db.Column(db.TIMESTAMP, name='datetime', nullable=False, comment='订单创建日期')
    deadline = db.Column(db.Date, comment='订单期限')

    forms = db.relationship('OrderForm', lazy='select', cascade="all, delete-orphan", backref='remarks')

    def __init__(self, company_id: int, remarks: str, deadline=None):
        self.company_id = company_id
        self.remarks = OrmVerity.verify_null_value(value=remarks, result=None)
        self.deadline = OrmVerity.verify_deadline(deadline=deadline)

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
