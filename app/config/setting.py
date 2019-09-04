# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
__author__ = 'lr'

# TOKEN过期时间 秒
TOKEN_EXPIRATION = 30 * 24 * 3600
# 配置本地存储图片的url前缀，云上的默认为整个连接
SERVER_URL = '172.16.50.143:8010'
IMG_PREFIX = SERVER_URL + '/static/images'
# 使用时os.path.join(UPLOAD_FOLDER)
UPLOAD_FOLDER = 'app/static/uploads'
VERSION = "0.0.1" # 项目版本

SWAGGER = {
	"swagger_version": "2.0",
	"info": {
		"title": "Flask RESTful API",
		"version": VERSION,
		"description": "A simple API to learn how to write OpenAPI Specification",
		"contact": {
			"responsibleOrganization": "Shema",
			"responsibleDeveloper": "lr",
			"email": "964157675@qq.com",
			"url": "https://github.com/linrong"
		},
		"termsOfService": "https://github.com/linrong"
	},
	"host": SERVER_URL,
	"basePath": "/",  # base bash for blueprint registration
	"tags": [], # 在'/app/api/v1/__init__.py'定义
	"schemes": [
		"http",
		"https"
	],
	"securityDefinitions": {
		'basicAuth': {
			'type': 'basic'
		}
	}
}