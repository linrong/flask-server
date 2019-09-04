# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, ForbiddenException
from app.libs.scope import is_in_scope

__author__ = 'lr'

"""
使用的是HTTPBasicAuth认证，暂时不清楚和HTTPTokenAuth有什么区别
不过上传的数据和生成的token有点不一样
上传的头文件：Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
获取到的token: "eyJhbGcioiJIUzUx...."
这两个之间的使用需要调研下,链接(http://www.bjhee.com/flask-ext9.html)
使用Postman中Authorization 设置使用 Basic Auth
使用Flassger中securityDefinitions 设置使用 basicAuth (详见config/setting.py)
"""
auth = HTTPBasicAuth() 
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


# 装饰器的使用，@auth.verify_password等于verify_password=auth.verify_password(verify_password)
# 所以即使没有调用verify_password，但访问此模块时auth.verify_password已经被调用
# 不明白可以查看decorated_example.py模块例子
@auth.verify_password
def verify_password(token, password):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        ''' 
            flask有四个上下文变量
			1.flask.current_app应用上下文，是当前app的示例对象
			2.flask.g应用上下文,处理请求时用作临时存储的对象
			3.flask.request请求上下文，封装客户端发出的HTTP请求内容
			4.flask.session请求上下文，存储用户对话
			请求上下文和应用上下文都是本地线程
			本地线程threading.local，可以理解为是在整个程序中一个共享的dict，每个线程中都可以获取到这个dict，
			但每个线程在自己的线程中从dict获取到的值都是自己线程独有的局部值，比如在一个线程①中定义threading.local.number=1,
			在另一个线程②中修改为threading.local.number=2，然后在①②线程中获取到的依然还是各自线程的值，分别为1，2
			
			flask的本地线程为werkzeug.local.Local，和threading.local有点不同：
			1.提供__storage__保存不同线程下的状态
			2.提供释放本地线程的release_loacl方法
			3.可以从greenlet/thread/_thread中依次尝试（try except）导入get_ident函数，用来获得线程或者协程标识符
			而且提供LocalStack和LocalProxy两种数据结构
        '''
        g.user = user_info
        return True

def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope'] # token处获得权限组信息
    # 可以获取要访问的视图函数,进行权限判断
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise ForbiddenException()
    return User(uid, ac_type, scope)
