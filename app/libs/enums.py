# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
__author__ = 'lr'

from enum import Enum
'''
	使用枚举
	1xx开头代表普通方式注册, 2xx代表第三方注册
'''


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201

class ScopeEnum(Enum):
	User = 1
	Admin = 2
	Super = 3