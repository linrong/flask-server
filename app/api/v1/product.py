# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
__author__ = 'lr'

from app.libs.error_code import Success, ProductException
from app.libs.redprint import RedPrint
from app.models.product import Product
from app.validators.params import Count, IDMustBePositiveInt

__author__ = 'lr'

api = RedPrint('product')


@api.route('/recent', methods=['GET'])
def get_recent():
	count = Count().validate_for_api().count.data
	products = Product.get_most_recent(count=count)
	return Success(products)

@api.route('/by_category', methods=['GET'])
def get_all_in_category():
	id = IDMustBePositiveInt().validate_for_api().id.data
	products = Product.get_product_by_category_id(id=id)
	return Success(products)