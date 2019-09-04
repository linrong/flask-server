# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/28.
"""
from sqlalchemy import Column, Integer, SmallInteger,String, Float, Text

from app.models.base import Base

__author__ = 'lr'

class Order(Base):
	id = Column(Integer, primary_key=True, autoincrement=True)
	order_no = Column(String(20), unique=True)
	user_id = Column(Integer)
	total_price = Column(Float)
	order_status = Column(SmallInteger, default=1)
	snap_img = Column(String(255))
	snap_name = Column(String(80))
	total_count = Column(Integer)
	snap_items = Column(Text)
	snap_address = Column(String(500))
	prepay_id = Column(String(100), unique=True)