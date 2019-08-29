# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from flask import Blueprint

from app.api.v2 import book, gift

__author__ = 'lr'

def create_blueprint_v2():
	bp_v2 = Blueprint('v2', __name__)
	book.api.register(bp_v2)
	gift.api.register(bp_v2)
	return bp_v2
