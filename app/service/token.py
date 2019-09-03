# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/28.
"""
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

__author__ = 'lr'

class Token():
	@staticmethod
	def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
		"""
		生成token，将用户的id，作用域，用户类型，过期时间写入token
		:param uid: 用户id
		:param ac_type: 用户类型
		:param scope: 权限域
		:param expiration: 过期时间 秒
		:return:
		"""
		s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
		token = s.dumps({
			'uid': uid,
			'type': ac_type.value,
			'scope': scope
		})
		return {'token': token.decode('ascii')}