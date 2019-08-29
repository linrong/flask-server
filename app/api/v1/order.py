# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/28.
"""
from app.libs.redprint import RedPrint
from app.libs.success_code import Success
from app.validators.params import OrderPlace

__author__ = 'lr'

api = RedPrint('order')


@api.route('', methods=['POST'])
def place_order():
    products = OrderPlace().validate_for_api().products.data
    return Success(products)


@api.route('/<int:id>', methods=['GET'])
def get_detail():
	pass


@api.route('/by_user', methods=['GET'])
def get_summary_by_user():
	pass


@api.route('/paginate', methods=['GET'])
def get_summary():
	pass


@api.route('/delivery', methods=['PUT'])
def delivery():
	pass