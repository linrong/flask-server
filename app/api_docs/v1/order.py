# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/30.
"""
__author__ = 'lr'

'''
"type": "array" 时
	- 可以使用 items
"type": 'object'时
	-可以使用 properties
'''
place_order = {
	"parameters": [
		{
			"name": "body",
			"in": "body",
			"require": "true",
			"schema": {
				"id": "Order", # 在Swagger中，可以显示Model; 全局唯一，否则会覆盖同ID处
				"required": ["products"],
				"properties": {
					"products": {
						"type": "array",
						"description": "商品列表",
						"items": {
							"type": 'object',
							"properties": {
								'product_id': {
									'type': 'integer',  # 不写 enum，则默认为数字0
									"enum": [1, 2, 3, 4, 5],  # 在Swagger中，默认显示第0个
									'default': 1  # 必须结合 enum 使用，否则无效; 可以自定义超出enum设置的范围
								},
								'count': {
									'type': 'integer',
									"enum": [10, 15, 20, 25, 30],
									'default': 10
								}
							}
						}
					}
				}
			}
		}
	],
	"security": [
		{
			"basicAuth": []
		}
	],
	"responses": {
		"200": {
			"description": "提交订单的结果",
			"examples": {}
		}
	}
}

get_detail = {
	"parameters": [],
	"responses": {
		"200": {
			"description": "产品分类",
			"examples": {}
		}
	}
}

get_summary_by_user = {
	"parameters": [],
	"responses": {
		"200": {
			"description": "产品分类",
			"examples": {}
		}
	}
}

get_summary = {
	"parameters": [],
	"responses": {
		"200": {
			"description": "产品分类",
			"examples": {}
		}
	}
}

delivery = {
	"parameters": [],
	"responses": {
		"200": {
			"description": "产品分类",
			"examples": {}
		}
	}
}