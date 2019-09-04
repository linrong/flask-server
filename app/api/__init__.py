# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/09/04.
"""
from app.api.v1 import create_api_tags_v1
from app.api.cms import create_api_tags_cms

__author__ = 'lr'

tags = create_api_tags_v1() + create_api_tags_cms() 