# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""

from .app import Flask

__author__ = 'lr'


def create_app():
	app = Flask(__name__)
	# 通过配置文件加载配置
	app.config.from_object('app.config.secure')
	app.config.from_object('app.config.setting')
	
	# 注册蓝图，有点像django中试视图和url的结合，不过这里是一起处理了的,而且这里使用自定义红图处理视图层函数,蓝图处理模块
	register_blueprint(app)
	register_plugin(app)

	return app


def register_plugin(app):
	from app.models.base import db
	db.init_app(app)
	with app.app_context():
		db.create_all()


def register_blueprint(app):
	from app.api.v1 import create_blueprint_v1
	app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')
