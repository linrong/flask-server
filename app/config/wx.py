# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/28.
"""
__author__ = 'lr'

APP_ID = 'wx551ff8259cd7339b'
APP_SECRET = '266db382ae9842940d292e0ce021182c'
LOGIN_URL = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'

# 微信·开放平台(OPEN)登录[第三方(Third-Party)]
OPEN_APP_ID = 'wx87186e0123456789'
OPEN_APP_SECRET = '606d686fa91edc283d9cd00123456789'
OPEN_SCOPE = 'snsapi_login'
OPEN_STATE = '3d6be0a4035d839573b04816624a415e'
REDIRECT_URI = 'https%3a%2f%2fapi.ivinetrue.com%2ftoken%2fuser'
OPEN_AUTHORIZE_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={0}&redirect_uri={1}&response_type=code&scope={2}&state={3}#wechat_redirect'.format(
	OPEN_APP_ID, OPEN_APP_SECRET, OPEN_SCOPE, OPEN_STATE
)
OPEN_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'
OPEN_USER_INFO_URL = 'https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}&lang=zh_CN'