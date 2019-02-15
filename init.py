"""
项目全局通用对象初始化文件
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()


def create_app():
    """创建app"""
    app = Flask(__name__)  # 创建app
    app.secret_key = config.APP_SECRET_KEY
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'mysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}/' \
        f'{config.MYSQL_NAME}'  # 链接app,db导入app时获取连接信息
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 如果设置成True(默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
    app.config['SQLALCHEMY_POOL_SIZE'] = 120
    app.config['SQLALCHEMY_ECHO'] = False  # 查看orm生成的语句
    return app
