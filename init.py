"""
项目全局通用对象初始化文件
"""
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
"""redis连接池
官方推荐使用StrictRedis方法
当使用了连接池,初始化设置都需要通过ConnectionPool传入参数.
设置了decode_responses,默认存入取出自动编码解码.也就是以str存入,str取出.存入int也会被转为str
"""
pool = redis.ConnectionPool(host=config.REDIS_HOST, port='6379', db=1, decode_responses=True)
Redis = redis.StrictRedis(connection_pool=pool)


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
