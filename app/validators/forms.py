# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseValidator

__author__ = 'lr'

'''
	用于参数校验,Flask为我们提供了一个wtforms的扩展专门来处理参数校验
'''


class ClientValidator(BaseValidator):
    # 账号
    account = StringField(validators=[DataRequired(message='Not Null'),
                                      length(min=5, max=32)])
    # 密码
    secret = StringField()
    # 注册类型
    type = IntegerField(validators=[DataRequired()])

    # 验证type是ClientTypeEnum中的
    # validate_xxx如果错误会把错误保存到form的error属性中，wtforms的form是不会将异常抛出的，这里我们统一在base的.validate()中抛出
    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        # 转化form.type.data为枚举类型
        self.type.data = client


class TokenValidator(BaseValidator):
    token = StringField(validators=[DataRequired()])


class UserEmailValidator(ClientValidator):
    account = StringField(validators=[Email(message='invalidate email')])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters, numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[
        DataRequired(),
        length(min=2, max=22)
    ])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchValidator(BaseValidator):
    q = StringField(validators=[DataRequired()])
