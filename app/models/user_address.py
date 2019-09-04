# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/28.
"""
from sqlalchemy import Column, Integer, String, ForeignKey

from app.models.base import Base

__author__ = 'lr'

class UserAddress(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
	name =  Column(String(30), nullable=False)
	mobile =  Column(String(20), nullable=False)
	country =  Column(String(20))
	province =  Column(String(20))
	city =  Column(String(20))
	detail =  Column(String(100)) # 具体体制

	def keys(self):
		# return ['id', 'email', 'nickname', 'auth', 'user_address']
		self.hide('id', 'user_id' )
		return self.fields