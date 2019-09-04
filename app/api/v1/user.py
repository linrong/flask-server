# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from flask import g

from app.libs.success_code  import DeleteSuccess, Success, RenewSuccess
from app.libs.redprint import RedPrint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User

__author__ = 'lr'

api = RedPrint(name='user', description='用户')

"""
装饰器的使用(https://www.liaoxuefeng.com/wiki/1016959663602400/1017451662295584)
装饰器的代码执行顺序(https://www.jianshu.com/p/a58d6f71b1ce)
"""
# 因为auth从app.libs.token_auth模块导入，所以auth.verify_password先于auth.login_required调用

@api.route('', methods=['GET'])
@api.doc()
@auth.login_required
def fetch_user():
	'''用户获取信息'''
	uid = g.user.uid  # g变量是「线程隔离」的
	user = User.query.filter_by(id=uid).first_or_404()
	return Success(user)


@api.route('', methods=['PUT'])
@api.doc()
@auth.login_required
def update_user():
	'''用户更新'''
	return RenewSuccess()


@api.route('', methods=['DELETE'])
@api.doc()
@auth.login_required
def delete_user():
	'''用户注销'''
	uid = g.user.uid  # g变量是「线程隔离」的
	with db.auto_commit():
		# 取代user = User.query.get_or_404(uid)，即使删除了还是能查到
		user = User.query.filter_by(id=uid).first_or_404()
		user.delete()
	return DeleteSuccess()