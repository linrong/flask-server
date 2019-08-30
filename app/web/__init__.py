# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/29.
"""
from flask import Blueprint

__author__ = 'lr'

web = Blueprint('web', __name__)

from app.web import auth