# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from flask import current_app

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed, Success
from app.libs.redprint import RedPrint
from app.models.user import User
from app.validators.forms import ClientValidator, TokenValidator
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
	SignatureExpired, BadSignature

__author__ = 'lr'

api = RedPrint('token')


@api.route('', methods=['POST'])
def get_token():
    # 获取token需要同时上传账号，密码，账号类型，即登录,数据的获取在ClientValidator的父类的init
	form = ClientValidator().validate_for_api()
	promise = {
		ClientTypeEnum.USER_EMAIL: User.verify,
    }
    # 判断用户是否存在并返回信息
	identity = promise[ClientTypeEnum(form.type.data)](form.account.data, form.secret.data)
	# Token生成
	expiration = current_app.config['TOKEN_EXPIRATION']
	token = generate_auth_token(identity['uid'],
								form.type.data,
								identity['scope'],
								expiration)
	# 注意需要进行 ascii 编码
	t = {'token': token.decode('ascii')}
	return Success(data=t)

@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    form = TokenValidator().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'], # 创建时间
        'expire_in': data[1]['exp'], # 有效期
        'uid': data[0]['uid']
    }
    return Success(data=r)


def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
	"""
    生成token，将用户的id，作用域，用户类型，过期时间写入token
    :param uid: 用户id
    :param ac_type: 用户类型
    :param scope: 权限域
    :param expiration: 过期时间 秒
    :return:
    """
	s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
	return s.dumps({
		'uid': uid,
		'type': ac_type.value,
		'scope': scope
	})
