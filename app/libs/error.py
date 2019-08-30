# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from flask import request, json
from werkzeug.exceptions import HTTPException

__author__ = 'lr'


class APIException(HTTPException):
	code = 500  # http 状态码
	msg = 'sorry, we make a mistake!' # 异常信息
	error_code = 999 # 约定的异常码

	def __init__(self, code=None, error_code=None, msg=None, headers=None):
		if code:
			self.code = code
		if error_code:
			self.error_code = error_code
		if msg:
			self.msg = msg
		super(APIException, self).__init__()
	
	# 重写构建返回错误主体为json，并使用自定义的属性名
	def get_body(self, environ=None):
		body = dict(
			msg= self.msg,
			error_code = self.error_code,
			request_url  = request.method + ' ' + self.get_url_no_param()
		)
		text = json.dumps(body) #返回文本
		return text
	
	# 重写错误返回类型为json
	def get_headers(self, environ=None):
		return[('Content-type', 'application/json; charset=utf-8')]
	
	# 返回不带参数的请求url
	@staticmethod
	def get_url_no_param():
		full_path = str(request.full_path)
		main_path = full_path.split('?')[0]
		return main_path

