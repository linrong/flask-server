# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from app.libs.success_message import Success
from app.libs.redprint import RedPrint
from app.models.category import Category

__author__ = 'lr'

api = RedPrint('category')


@api.route('/all', methods=['GET'])
def get_all_categories():
	categories = Category.get_all_categories()
	return Success(categories)
