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
		data = request.get_json(silent=True)
		view_args = _request_ctx_stack.top.request.view_args  # 获取view中的args
		args = dict(request.args.to_dict(), **view_args)
		super(BaseValidator, self).__init__(data=data, **args)

	def validate_for_api(self):
		valid = super(BaseValidator, self).validate()
		if not valid:
			raise ParameterException(msg=self.errors)
		return self

	def isPositiveInteger(self, value):
		return True if (value.isdigit() and int(value) > 0) else False
