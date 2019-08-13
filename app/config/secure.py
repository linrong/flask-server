# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
__author__ = 'lr'

# 开启debug模式,应该只用在开发环境
DEBUG = True 
# 数据库连接
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:159951@localhost:3306/zerd?charset=utf8'
# SECRET_KEY配置变量是通用密钥，可在Flask和多个第三方扩展中使用。如其名所示，加密的强度取决与变量值的机密度。不同的程序使用不同的密钥，而且要保证其他人不知道你所用的字符串
SECRET_KEY = 'But you, Lord , are a shield around me, my glory, the One who lifts my head high.'
