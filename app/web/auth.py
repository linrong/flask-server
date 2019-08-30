# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/29.
"""
from flask import render_template, redirect
from . import web

__author__ = 'lr'

# 因为在app中注册的时候没有配置url的前缀,所以访问文档的连接为172.16.50.431:8010
@web.route('/')
def index():
    '''默认跳转的 API 文档'''
    return redirect('/apidocs/#/')
    # return render_template("index.html")