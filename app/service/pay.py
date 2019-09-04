# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/09/03.
"""
from flask import g

from app.libs.enums import OrderStatusEnum
from app.libs.error_code import OrderException, TokenException
from app.models.user import User
from app.service.order import Order as OrderService
from app.service.token import Token
from app.models.order import Order as OrderModel

__author__ = 'lr'

class Pay():
	order_id = None
	order_no = None

	def __init__(self, order_id):
		if not order_id:
			# todo
			raise Exception('订单号不允许为NULL') # '订单号不允许为NULL'
		self.order_id = order_id

	def pay(self):
		# 检测订单情况
		self.__check_order_valid()
		# 支付前，再次进行库存量检测
		order_service = OrderService()
		status = order_service.check_order_stock(self.order_id)
		if not status['pass']:
			return status
		return self.__make_wx_pre_order(status['order_price'])
	
	def __make_wx_pre_order(self, order_price):
		user = User.query.filter_by(id=g.user.uid).first_or_404()
		openid = user.openid
		if not openid:
			# openid不存在
			pass
		wx_order_data = None
		return self.__get_pay_signature(wx_order_data)

	def __get_pay_signature(self, wx_order_data):
		'''签名'''
		wx_order = None
		if wx_order['return_code'] != 'SUCCESS' or wx_order['result_code'] != 'SUCCESS':
			pass # 记录到日志里
		return None

	def __check_order_valid(self):
		'''对订单作三种情况的检测'''
		# 1. 验证订单号是否存在
		order = OrderModel.query.filter_by(id=self.order_id).first_or_404(e=OrderException)
		# 2. 如果订单号存在的，验证订单号与当前用户是否匹配
		if not Token.is_valid_operate(order.user_id):
			raise TokenException(msg='订单与用户不匹配', error_code=1003)
		# 3. 验证订单是否已经被支付过
		if order.order_status != OrderStatusEnum.UNPAID:
			raise OrderException(
				msg='订单已支付',
				error_code=8003,
				code=404
			)
		self.order_no = order.order_no
		return True