# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
__author__ = 'lr'

from enum import Enum

class ClientTypeEnum(Enum):
	USER_EMAIL = 100
	USER_MOBILE = 101

	# 微信小程序
	USER_MINA = 200
	# 微信公众号
	USER_WX = 201
