# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from app.libs.limiter import cached
from app.libs.success_code  import Success
from app.libs.redprint import RedPrint
from app.models.theme import Theme
from app.validators.params import IDCollection, IDMustBePositiveInt

__author__ = 'lr'

api = RedPrint(name='theme', description='主题')

@api.route('', methods=['GET'])
@api.doc()
@cached()
def get_simple_list():
	'''一组 ID 的专题(Theme)
	:url /theme
	:arg /theme?ids=id1,id2,id3,...
	:return: 一组theme模型
	'''
	ids = IDCollection().validate_for_api().ids.data
	theme = Theme.get_themes(ids=ids)
	return Success(theme)


@api.route('/<int:id>', methods=['GET'])
@api.doc()
@cached()
def get_complex_one(id):
	'''专题(Theme)详情接口
	Theme详情接口
	:url /theme/:id
	:param id: 专题theme的id
	:return: 专题theme的详情
	'''
	id = IDMustBePositiveInt().validate_for_api().id.data
	theme_detail = Theme.get_theme_detail(id=id)
	return Success(theme_detail)
