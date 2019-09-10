# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from collections import namedtuple
import os

from flask import current_app
from werkzeug.datastructures import FileStorage
from wtforms import StringField, IntegerField, FileField, MultipleFileField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseValidator

__author__ = 'lr'

'''
	用于参数校验,Flask为我们提供了一个wtforms的扩展专门来处理参数校验
'''
Address = namedtuple('Address', ['name', 'mobile', 'province', 'city', 'country', 'detail'])

# BaseValidator的init中进行数据获取
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


class UploadFileValidator(BaseValidator):
    origin = FileField(validators=[DataRequired()])
    comparer = FileField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])

    def get_size(self,file_obj: FileStorage):
        """
        得到文件大小（字节）
        :param file_obj: 文件对象
        :return: 文件的字节数
        """
        file_obj.seek(0, os.SEEK_END)
        size = file_obj.tell()
        file_obj.seek(0)  # 将文件指针重置
        return size

    def validate_origin(self,value):
        default_config = current_app.config.get('FILE')
        if value.data:
            # 判断文件格式
            if '.' not in value.data.filename or \
                value.data.filename.rsplit('.', 1)[1] not in default_config['INCLUDE']:
                raise ValidationError('文件格式错误')
            if self.get_size(value.data) >  default_config['SINGLE_LIMIT']:
                raise ValidationError('文件大小错误')


class AddressNew(BaseValidator):
    name = StringField(validators=[DataRequired()])
    mobile = StringField(validators=[           
        DataRequired(),
        length(min=11, max=11, message='手机号为11个数字'),
        Regexp(r'^1(3|4|5|7|8)[0-9]\d{8}$')
    ])
    province = StringField(validators=[DataRequired()])
    city = StringField(validators=[DataRequired()])
    country = StringField(validators=[DataRequired()])
    detail = StringField()

    @property
    def data(self):
        return Address(
			self.name.data, self.mobile.data, self.province.data,
			self.city.data, self.country.data, self.detail.data
		)

class PaginateValidator(BaseValidator):
	page = IntegerField(default=1)
	size = IntegerField(default=10)

	def validate_page(self, value):
		self.page.data = int(value.data)

	def validate_size(self, value):
		self.size.data = int(value.data)