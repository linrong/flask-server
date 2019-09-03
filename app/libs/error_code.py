# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from app.libs.error import APIException

__author__ = 'lr'


class ClientTypeError(APIException):
	code = 400
	error_code = 1006
	msg = 'clinet is invalid'


class ServerError(APIException):
	code = 500
	error_code = 999
	msg = 'sorry, we make a mistake!'


class WeChatException(ServerError):
	code = 500
	error_code = 999
	msg = '微信服务器接口调用失败'


class ParameterException(APIException):
	code = 400
	error_code = 1000
	msg = 'invalid parameter'

class TokenException(APIException):
	code = 401
	error_code = 1001
	msg = 'Token已过期或无效Token'

class AuthFailed(APIException):
	code = 401
	error_code = 1005
	msg = 'authorization failed'


class ForbiddenException(APIException):
	code = 403
	error_code = 1004
	msg = 'forbidden, not in scope'


class DuplicateException(APIException):
	code = 400
	error_code = 2001
	msg = 'data duplication'


class NotFound(APIException):
	code = 404
	error_code = 1001
	msg = 'the resource are not found'

	def __init__(self, error_code=None, msg=None):
		if error_code:
			self.error_code = error_code
		if msg:
			self.msg = msg
		super(NotFound, self).__init__()


class ProductException(NotFound):
	code = 404
	error_code = 2000
	msg = '指定的商品不存在，请检查参数'


class ThemeException(NotFound):
	code = 404
	error_code = 3000
	msg = '请求的主题不存在，请检查主题ID'


class BannerMissException(NotFound):
	code = 404
	error_code = 4000
	msg = '请求的Banner不存在'


class CategoryException(NotFound):
	code = 404
	error_code = 5000
	msg = '指定的类目不存在, 请检查参数'


class UserException(NotFound):
	code = 404
	error_code = 6000
	msg = '用户不存在'


class OrderException(NotFound):
	code = 404
	error_code = 8000
	msg = '订单不存在，请检查ID'
