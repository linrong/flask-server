# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base
from app.models.image import Image

__author__ = 'lr'

class Theme2Product(Base):
	__tablename__ = 'theme_product'
	theme_id = Column(Integer, ForeignKey('theme.id'), primary_key=True)
	product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)


class Product2Image(Base):
	__tablename__ = 'product_image'
	id = Column(Integer, primary_key=True, autoincrement=True)
	img_id = Column(Integer, ForeignKey('image.id'), nullable=False)
	order = Column(Integer, nullable=False)
	product_id = Column(Integer, ForeignKey('product.id'), nullable=False)

	def keys(self):
		self.hide('id','img_id', 'product_id', 'order').append('img_url')
		return self.fields

	@property
	def img_url(self):
		return Image.get_img_by_id(id=self.img_id).url


class Product2Property(Base):
	__tablename__ = 'product_property'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(30))
	detail = Column(String(255), nullable=False)
	product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
