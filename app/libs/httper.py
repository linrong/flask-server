# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/28.
"""
__author__ = 'lr'

import requests

class HTTP:
	@staticmethod
	def get(url, return_json=True):
		res = requests.get(url)
		if res.status_code != 200:
			return {} if return_json else ''
		return res.json() if return_json else res.text