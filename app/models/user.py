# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.enums import ScopeEnum
from app.libs.error_code import AuthFailed
from app.models.base import Base, db
from app.models.user_address import UserAddress
from app.service.user_token import UserToken

__author__ = 'lr'


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(50), unique=True)
    email = Column(String(24), unique=True)
    nickname = Column(String(24), unique=True)
    extend = Column(String(255))
    # 区分管理员和普通用户，1为普通用户，2为管理员
    auth = Column(SmallInteger, default=1)
    _user_address = db.relationship('UserAddress', backref='author', lazy='dynamic')
    _password = Column('password', String(100))

    # model中增加keys方法是为了在序列化时使用dict(xxx)方式序列化model
    # __getitem__也要加，不过统一加在父类Base中
    # 当keys返回的是tuple并且只有一个属性时记着别忘了加,，否则会得到这样一个错误Object has no attribute 'n'.
    def keys(self):
        # return ['id', 'email', 'nickname', 'auth'] # 返回的类型要是tuple,或者list等序列类型
        self.hide('openid', '_password', 'extend').append('user_address')
		return self.fields

    @property
    def password(self):
        return self._password

	@property
	def user_address(self):
		return self._user_address.first()

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def save_address(self, address_info):
        with db.auto_commit():
            # address = UserAddress.query.filter_by(user_id=self.id).first()
            address = self._user_address.first()
            if not address:
                address = UserAddress(author=self)
            address.user_id = self.id
            address.name = address_info.name
            address.mobile = address_info.mobile
            address.province = address_info.province
            address.city = address_info.city
            address.country = address_info.country
            address.detail = address_info.detail
            db.session.add(address)

    @staticmethod
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def register_by_wx(account):
        with db.auto_commit():
            user = User()
            user.openid = account
            db.session.add(user)
        return User.query.filter_by(openid=account).first()

    @staticmethod
    def verify_by_email(email, password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == ScopeEnum.Admin else 'UserScope' # 判断用户是否为管理员,用于生成token时返回权限组信息添加到token处
        return {'uid': user.id, 'scope': scope}

    @staticmethod
    def verify_by_wx(code, *args):
        ut = UserToken(code)
        wx_result = ut.get()
        openid = wx_result['openid']
        user = User.query.filter_by(openid=openid).first()
        if not user:
            user = User.register_by_wx(openid)
        scope = 'AdminScope' if user.auth == ScopeEnum.Admin else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
