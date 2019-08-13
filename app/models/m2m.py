# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import Base

__author__ = 'lr'

class Theme2Product(Base):
	__tablename__ = 'theme_product'
	theme_id = Column(Integer, ForeignKey('theme.id'), primary_key = True)
	product_id = Column(Integer, ForeignKey('product.id'), primary_key = True)
