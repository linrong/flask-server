# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/26.
"""
from flask import g

from app.libs.error_code import UserException
from app.libs.success_message import RenewSuccess
from app.libs.redprint import RedPrint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User
from app.validators.forms import AddressNew

__author__ = 'lr'

api = RedPrint('address')


@api.route('', methods=['POST'])
@auth.login_required
def renew_address():
	address_info = AddressNew().validate_for_api().data
	uid = g.user.uid
	with db.auto_check_empty(UserException):
		user = User.query.filter_by(id=uid).first_or_404()
	user.save_address(address_info)
	return RenewSuccess()