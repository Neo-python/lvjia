"""通用模型模块"""
from init import db


class Common(object):
    """orm通用操作"""

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

    def __str__(self):
        return f'<class \'{self.__name__}\' id={self.id}>'


class Company(db.Model, Common):
    """公司模型"""
    __tablename__ = 'company'
    id = db.Column(db.Integer, index=True, primary_key=True)

    name = db.Column(db.String(length=50), nullable=False, unique=True, comment='公司/单位名')
    address = db.Column(db.String(length=255), comment='公司/单位地址')

    personnel = db.relationship('People', lazy=True, cascade="all, delete-orphan", backref='feature')

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

    def __repr__(self):
        return f'id={self.id}, name={self.name}, address={self.address}'


class Product(db.Model, Common):
    """产品模型"""
    __tablename__ = 'product'
    id = db.Column(db.Integer, index=True, primary_key=True)

    name = db.Column(db.String(length=50), nullable=False, comment='产品名')
    price = db.Column(db.DECIMAL(precision=9, decimal_return_scale=2), default=0.00, nullable=False, comment='产品单价')
    unit = db.Column(db.SMALLINT, nullable=False, default=0, comment='产品单位,0:千克 1:个')

    def __init__(self, name: str, price: float, unit: int = None):
        self.name = name
        self.price = price
        self.unit = unit

    def __repr__(self):
        return f'id={self.id}, name={self.name}, price={self.price}, unit={self.unit}'


class People(db.Model, Common):
    """人员模型"""
    __tablename__ = 'people'
    id = db.Column(db.Integer, index=True, primary_key=True)

    name = db.Column(db.String(length=50), nullable=False, comment='人名')
    telephone = db.Column(db.String(length=13), nullable=False, comment='联系方式')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    remarks = db.Column(db.String(length=255), default='', comment='人员备注')

    def __init__(self, name: str, telephone: str, company_id: int, remarks: str = None):
        self.name = name
        self.telephone = telephone
        self.company_id = company_id
        self.remarks = remarks

    def __repr__(self):
        return f'id={self.id}, name={self.name}, telephone={self.telephone}, company_id={self.company_id}, remarks={self.remarks}'


class ExternalPrice(db.Model, Common):
    """公司/单位专价模型"""
    __tablename__ = 'external_price'
    id = db.Column(db.Integer, index=True, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    price = db.Column(db.DECIMAL(precision=9, decimal_return_scale=2), default=0.00, nullable=False, comment='产品单价')

    def __init__(self, product_id: int, company_id: int, price: float):
        self.product_id = product_id
        self.company_id = company_id
        self.price = price

    def __repr__(self):
        return f'id={self.id}, product_id={self.product_id}, company_id={self.company_id}, price={self.price}'
