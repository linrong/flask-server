# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from sqlalchemy import Column, Integer, Float, String, SmallInteger
from sqlalchemy import desc, asc
from sqlalchemy.orm import relationship, backref

from app.libs.error_code import ProductException
from app.libs.utils import jsonify
from app.models.m2m import Theme2Product, Product2Image
from app.models.base import Base, db

__author__ = 'lr'

class Product(Base):
	__tablename__ = 'product'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(50))
	price = Column(Float)
	stock = Column(Integer)
	category_id = Column(Integer)
	_main_img_url = Column('main_img_url', String(255))
	_from = Column('from', SmallInteger, default=1)
	summary = Column(String(50))
	img_id = Column(Integer)
	theme = relationship('Theme', secondary='theme_product', backref=backref('product', lazy='dynamic'))

	def keys(self):
		self.hide('_main_img_url', '_from', 'img_id').append('main_img_url', 'img_urls')
		return self.fields

	@property
	def main_img_url(self):
		return self.get_url(self._main_img_url)

	@property
	def img_urls(self):
		try:
			img_urls = Product2Image.query.filter_by(product_id=self.id).order_by(asc(Product2Image.order)).all()
		except Exception:
			return []
		return list(map(lambda x: x['img_url'], jsonify(img_urls)))


	@staticmethod
	def get_most_recent(count):
		with db.auto_check_empty(ProductException):
			return Product.query.order_by(desc(Product.create_time)).limit(count).all()

	@staticmethod
	def get_product_by_category_id(id):
		with db.auto_check_empty(ProductException):
			return Product.query.filter_by(category_id=id).all()
	
	@staticmethod
	def get_product_detail(id):
		with db.auto_check_empty(ProductException):
			return Product.query.filter_by(id=id).first_or_404().hide('category_id')
