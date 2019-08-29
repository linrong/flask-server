# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""

from .app import Flask
from flask_cors import CORS

__author__ = 'lr'


def create_app():
    app = Flask(__name__)
    # 通过配置文件加载配置
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.wx')

    # 注册蓝图，有点像django中试视图和url的结合，不过这里是一起处理了的,而且这里使用自定义红图处理视图层函数,蓝图处理模块
    register_blueprint(app)
    register_plugin(app)
    
    cors = CORS()
    cors.init_app(app, resources={"/*": {"origins": "*"}})

    return app


def register_plugin(app):
    # 在model中用到了sqlalchemy这个第三方package, 所有的第三方package都需要注册到Flask核心对象上才会起作用,创建一个函数用来将其注册到Flask核心对象上
    from app.models.base import db
    db.init_app(app)
    # db.create_all()方法只能在Flask核心对象的上下文栈中才会起作用. 所以我们要用with调用Flask核心对象的app_context()方法将其推入Flask核心对象的上下文栈中
    with app.app_context():
        # 如果数据库表已经存在于数据库中, 那么 db.create_all() 不会创建或更新这个表
        db.create_all()


def register_blueprint(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')
