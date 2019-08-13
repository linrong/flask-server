# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from app import create_app

__author__ = 'lr'
from app.models.base import db
from app.models.user import User

app = create_app()
with app.app_context():
    with db.auto_commit():
        # 创建一个超级管理员
        user = User()
        user.email = '999@qq.com'
        user.nickname = 'Super'
        user.auth = 2
        user.password = '123456'
        db.session.add(user)
