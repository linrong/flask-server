# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from datetime import date

from flask import Flask as _Flask, _request_ctx_stack
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.error_code import ServerError

__author__ = 'lr'


class JSONEncoder(_JSONEncoder):
	def default(self, o):
		# hasattr() 函数用于判断对象是否包含对应的属性，返回True或者Flase
		if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
			# 序列化我们要返回的对象,主要是model里面的数据,并且要把keys方法和__getitme__方法放在了models中
			# 是获取keys中值进行字典化?keys控制要返回的字段
			return dict(o) 
		# isinstance()判断一个对象是否是一个已知的类型,其返回值为布尔型（True or flase）
		if isinstance(o, date):
			return o.strftime('%Y-%m-%d')
		# raise 关键字用于引发一个异常，基本上和C#和Java中的throw关键字相同
		# 一旦执行了raise语句，raise后面的语句将不能执行
		raise ServerError()




class Flask(_Flask):
	# json_encoder使用重写的JSONEncoder
	json_encoder = JSONEncoder