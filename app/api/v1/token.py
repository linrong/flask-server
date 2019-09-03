# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from flask import current_app

from app.libs.enums import ClientTypeEnum
from app.libs.success_code  import Success
from app.libs.redprint import RedPrint
from app.models.user import User
from app.service.token import Token
from app.validators.forms import ClientValidator, TokenValidator

__author__ = 'lr'

api = RedPrint(name='token', description='令牌')


@api.route('/user', methods=['POST'])
@api.doc()
def get_token():
    '''生成「令牌」'''
    # 获取token需要同时上传账号，密码，账号类型，即登录,数据的获取在ClientValidator的父类的init
    form = ClientValidator().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify_by_email,
        ClientTypeEnum.USER_WX: User.verify_by_wx,
    }
    # 判断用户是否存在并返回信息
    # 微信登录则account为code(需要微信小程序调用wx.login接口获取), secret为空
    identity = promise[ClientTypeEnum(form.type.data)](form.account.data, form.secret.data)
	# Token生成
    expiration = current_app.config['TOKEN_EXPIRATION'] # token有效期
    token = Token.generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)
    return Success(data=token)


@api.route('/app', methods=['POST'])
def get_app_token():
	pass


@api.route('/secret', methods=['POST'])
@api.doc()
def get_token_info():
    """解析「令牌」"""
    token = TokenValidator().validate_for_api().token.data
    result = Token.decrypt(token)
    return Success(data=result)
