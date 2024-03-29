# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from flask import request, _request_ctx_stack
from wtforms import Form, ValidationError

from app.libs.error_code import ParameterException

__author__ = 'lr'


class BaseValidator(Form):
	def __init__(self):
		# 这里接收了request携带的数据，然后用于检验
		# 1.只接收application/json的json数据
		json_data = request.get_json(silent=True) 
		# 2.接收multipart/form-data里面的file和text
		form_data = dict(request.files.to_dict(),**request.form.to_dict())
		# 理论上来说不会同时上传multipart/form-data和application/json中的数据
		if json_data:
    			form_data.update(json_data)
		view_args = _request_ctx_stack.top.request.view_args # 获取view中(path路径里)的args
		args = dict(request.args.to_dict(), **view_args) # query中: request.args.to_dict()
		super(BaseValidator, self).__init__(data=form_data, **args)

	def validate_for_api(self):
		# validate方法会对我们的所有字段进行迭代并且调用行内验证方法进行验证, 遇到validate_xxx继续调用行内验证方法验证, 具体关于wtforms的validate方法参考wtforms validate解释.
		# http://greyli.com/how-custom-validator-work-in-wtforms/
		# 调用BaseValidator父类的validate方法
		valid = super(BaseValidator, self).validate()
		if not valid:
			# 验证错误处理,抛出错误,self.errors即为validate_xx中抛出的错误
			raise ParameterException(msg=self.errors)
		return self

	def isPositiveInteger(self, value):
		try:
			value=int(value)
		except ValueError:
			return False
		return True if (isinstance(value, int) and value > 0) else False
	
	def isList(self, value):
		return True if isinstance(value, list) else False 
