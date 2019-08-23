# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
__author__ = 'lr'


class Scope:
	allow_api = []
	allow_module = []
	forbidden = []

    # __add__方法(即+)重写
	def __add__(self, other):
		# 去重
		self.allow_api = list(set(self.allow_api + other.allow_api))
		self.allow_module = list(set(self.allow_module + other.allow_module))
		self.forbidden = list(set(self.forbidden + other.forbidden))

		return self


class UserScope(Scope):
	forbidden = ['v1.user+super_fetch_user', 'v1.user+super_delete_user',
				 'v1.user+super_update_user']

	def __init__(self):
		# 利用内置的__add__方法叫做运算符重载
		self + AdminScope()


class AdminScope(Scope):
	# allow_api = ['v1.user+super_fetch_user', 'v1.user+super_delete_user']
	allow_module = ['v1.user']  # 所有视图函数

	def __init__(self):
		# self + (UserScope())
		pass


class SuperScope(Scope):
	allow_api = []
	allow_module = []

	def __init__(self):
		self + UserScope() + AdminScope()


def is_in_scope(scope, endpoint):
	scope = globals()[scope]() # 使用字符串scope动态创建对象scope：globals()函数返回一个dict, 我们的模块下的所有变量和对象都是dict的key, 包括UserScope和AdminScope等对象
	splits = endpoint.split('+')
	red_name = splits[0]  # v1.*
	if endpoint in scope.forbidden:
		return False
	if endpoint in scope.allow_api:
		return True
	if red_name in scope.allow_module:
		return True
	else:
		return False
