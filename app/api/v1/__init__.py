# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from flask import Blueprint

from app.api.v1 import user, client, token, \
						banner, theme, product, category, \
						address, order, pay

__author__ = 'lr'

def create_blueprint_v1():
	bp_v1 = Blueprint('v1', __name__)
	# 自定义红图，用来拆分视图函数层，然后红图注册到蓝图，蓝图用来拆分模块
	# 将红图注册进 蓝图bp_v1
	user.api.register(bp_v1)
	client.api.register(bp_v1)
	token.api.register(bp_v1)
	banner.api.register(bp_v1)
	theme.api.register(bp_v1)
	product.api.register(bp_v1)
	category.api.register(bp_v1)
	address.api.register(bp_v1)
	order.api.register(bp_v1)
	pay.api.register(bp_v1)
	return bp_v1

def create_api_tags_v1():
	'''
	Swagger API 文档分类
	数组中的顺序代表 Swagger 中的顺序
	'''
	return [
		token.api.tag,
		user.api.tag,
		client.api.tag,
		banner.api.tag,
		theme.api.tag,
		product.api.tag,
		category.api.tag,
		address.api.tag,
		order.api.tag,
		pay.api.tag,
	]
