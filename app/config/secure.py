# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
__author__ = 'lr'

"""
# 数据库连接方式
# 1.直接使用驱动写原生
python2+mysql-python(import MySQLdb)+mysql
python3+pyMysql(import pymysql)+mysql

# 2.使用orm，用SQLAlchemy为例子
python3+SQLAlchemy+pyMysql(import pymysql)+mysql

# 3.flask使用里面使用flask-SQLAlchemy更加方便使用orm
python3+flask-SQLAlchemy+SQLAlchemy+pyMysql(import pymysql)+mysql

# python3连接mysql包：pymysql，mysqlclient(就是Python3版本的MySQLdb),cymysql（fork of pymysql with optional C speedups）
"""

# 开启debug模式,应该只用在开发环境
DEBUG = True 
# 数据库连接，加载进falsk的config中后，应该在使用 db.init_app(app)时会使用连接数据库，是Flask-SQLAlchemy扩展需要的
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://flask:flask.com@db:3306/flask'
SQLALCHEMY_TRACK_MODIFICATIONS = True
# SECRET_KEY配置变量是通用密钥，可在Flask和多个第三方扩展中使用。如其名所示，加密的强度取决与变量值的机密度。不同的程序使用不同的密钥，而且要保证其他人不知道你所用的字符串
SECRET_KEY = 'But you, Lord , are a shield around me, my glory, the One who lifts my head high.'
