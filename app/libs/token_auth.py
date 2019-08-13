# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
	as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, ForbiddenException
from app.libs.scope import is_in_scope

__author__ = 'lr'

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])

@auth.verify_password
def verify_password(token, password):
	user_info = verify_auth_token(token)
	if not user_info:
		return False
	else:
		g.user = user_info
		return True

def verify_auth_token(token):
	s = Serializer(current_app.config['SECRET_KEY'])
	try:
		data = s.loads(token)
	except BadSignature:
		raise AuthFailed(msg='token is invalid', error_code=1002)
	except SignatureExpired:
		raise AuthFailed(msg='token is expired', error_code=1003)
	uid = data['uid']
	ac_type = data['type']
	scope = data['scope']
	# 可以获取要访问的视图函数
	allow = is_in_scope(scope, request.endpoint)
	if not allow:
		raise ForbiddenException()
	return User(uid, ac_type, scope)
