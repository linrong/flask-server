# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
__author__ = 'lr'

from app.libs.token_auth import auth
from app.libs.success_code  import Success,DeleteSuccess
from app.libs.redprint import RedPrint
from app.models.product import Product
from app.validators.params import Count, IDMustBePositiveInt

__author__ = 'lr'

api = RedPrint(name='product', description='产品')


@api.route('/recent', methods=['GET'])
@api.doc()
def get_recent():
	'''最新的商品'''
	count = Count().validate_for_api().count.data
	products = Product.get_most_recent(count=count)
	return Success(products)

@api.route('/by_category', methods=['GET'])
@api.doc()
def get_all_in_category():
	'''所有 category_id 类的商品'''
	id = IDMustBePositiveInt().validate_for_api().id.data
	products = Product.get_product_by_category_id(id=id)
	return Success(products)

@api.route('/<int:id>', methods=['GET'])
@api.doc()
def get_one(id):
	id = IDMustBePositiveInt().validate_for_api().id.data
	product = Product.get_product_detail(id=id)
	return Success(product)

@api.route('/<int:id>', methods=['DELETE'])
@api.doc()
@auth.login_required
def delete_one(id):
	'''删除某商品'''
	id = IDMustBePositiveInt().validate_for_api().id.data
	product = Product.get_product_detail(id=id)
	return DeleteSuccess()