# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from flask import Blueprint

__author__ = 'lr'

def create_blueprint_v2():
	bp_v1 = Blueprint('v2', __name__)
	return bp_v1
