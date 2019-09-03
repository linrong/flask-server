# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/09/03.
  「pay接口」只能用户访问，CMS管理员不能反问
"""
from app.libs.redprint import RedPrint
from app.libs.token_auth import auth
from app.validators.params import IDMustBePositiveInt

__author__ = 'lr'

api = RedPrint(name='pay', description='支付')

@api.route('pre_order', methods=['POST'])
@api.doc()
@auth.login_required
def get_pre_order():
	'''获取预订单'''
	id = IDMustBePositiveInt().validate_for_api().id.data
	pass