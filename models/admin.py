"""管理员层模型"""
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Common


class Admin(Common, db.Model):
    """管理员模型"""
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)

    account = db.Column(db.String(length=50), nullable=False, comment='账户')
    password = db.Column(db.String(length=255), nullable=False, comment='密码')
    level = db.Column(db.SMALLINT, nullable=False, comment='权限等级,0:普通权限.1:最高权限')
    phone = db.Column(db.String(length=11), nullable=False, comment='手机号')
    token = db.Column(db.String(length=32), nullable=False, comment='二级密码')

    def set_password(self, password: str):
        """设置密码
        :param password: string密码
        :return: None
        """
        if len(password) > 6:  # 不允许设置密码长度过短的密码
            self.password = generate_password_hash(password=password)
            self.direct_update_()
        else:
            raise ValueError('密码长度过短')

    def check_password(self, password: str) -> bool:
        """验证密码
        :param password: string密码
        :return: False:密码错误 True:验证通过
        """
        return check_password_hash(self.password, password=password)

    @staticmethod
    def login(account: str, password: str):
        """登入账户
        :param account: 账号
        :param password: string密码
        :return: None:账号错误 False:密码错误 True:验证通过,返回模型实例
        """
        admin = Admin.query.filter_by(account=account).first()
        if not admin:
            return None

        if admin.check_password(password=password):
            return admin
        else:
            return False

    @staticmethod
    def verify_token(token: str, self_token: str) -> bool:
        """验证二级密码"""
        md5 = hashlib.md5()
        md5.update(token.encode())
        hash_token = md5.hexdigest()
        return hash_token == self_token
