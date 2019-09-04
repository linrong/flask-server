# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.enums import ScopeEnum
from app.libs.error_code import AuthFailed, UserException
from app.models.base import Base, db
from app.models.user_address import UserAddress
from app.service.open_token import OpenToken
from app.service.user_token import UserToken

__author__ = 'lr'


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(50), unique=True)
    unionid = Column(String(50), unique=True)
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
        self.hide('openid', 'unionid', '_password', 'extend').append('user_address')
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
        """邮箱注册"""
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def register_by_wx(account):
        '''小程序注册
        在SQLAlchemy中一个Session（可以看作）是一个transaction，每个操作（基本上）对应一条或多条SQL语句，这些SQL语句需要发送到数据库服务器才能被真正执行，
        而整个transaction需要commit才能真正生效，如果没提交，一旦你的程序挂了，所有未提交的事务都会被回滚到事务开始之前的状态。
        flush就是把客户端尚未发送到数据库服务器的SQL语句发送过去，预提交，等于提交到数据库内存，还未写入数据库文件,commit就是告诉数据库服务器提交事务,把内存里面的东西直接写入。
        简单说，flush之后你才能在这个Session中看到效果，而commit之后你才能从其它Session中看到效果。
        '''
        with db.auto_commit():
            user = User()
            user.openid = account
            db.session.add(user)
            db.session.flush()
        return user

    @staticmethod
    def register_by_wx_open(user_info):
        """微信第三方注册"""
        img_filename = HTTP.download_pic(user_info['headimgurl'], type='avatar')
        with db.auto_commit():
            user = User()
            user.openid = user_info['openid']
            user.unionid = user_info['unionid']
            user.nickname = user_info['nickname']
            # user.avatar = img_filename
            db.session.add(user)
            db.session.flush()
        return user

    @staticmethod
    def verify_by_email(email, password):
        user = User.query.filter_by(email=email).first_or_404(
			e=UserException(msg='该账号未注册'))
        if not user.check_password(password):
            raise AuthFailed(msg='密码错误')
        scope = 'AdminScope' if user.auth == ScopeEnum.Admin else 'UserScope' # 判断用户是否为管理员,用于生成token时返回权限组信息添加到token处
        return {'uid': user.id, 'scope': scope}

    @staticmethod
    def verify_by_wx(code, *args):
        ut = UserToken(code)
        wx_result = ut.get() # wx_result = {session_key, expires_in, openid}
        openid = wx_result['openid']
        user = User.query.filter_by(openid=openid).first()
        # 如果不在数据库，则新建用户
        if not user:
            user = User.register_by_wx(openid)
        scope = 'AdminScope' if user.auth == ScopeEnum.Admin else 'UserScope'
        return {'uid': user.id, 'scope': scope}
    
    @staticmethod
    def verify_by_wx_open(code, *args):
        # 微信开放平台(第三方)登录
        ot = OpenToken(code)
        user_info  = ot.get()
        openid = user_info ['openid']  # 用户唯一标识
        user = User.query.filter_by(openid=openid).first()
        if not user:
            user = User.register_by_wx_open(user_info)
        scope = 'AdminScope' if ScopeEnum(user.auth) == ScopeEnum.Admin else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
