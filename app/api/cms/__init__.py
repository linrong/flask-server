# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/09/04.
"""
__author__ = 'lr'

from flask import Blueprint

from app.api.cms import user, file


def create_blueprint_cms():
    bp_cms = Blueprint('cms', __name__)
    user.api.register(bp_cms)
    file.api.register(bp_cms)

    return bp_cms


def create_api_tags_cms():
	return [
		user.api.tag,
		file.api.tag
	]