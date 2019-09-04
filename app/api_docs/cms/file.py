# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/29.
"""
__author__ = 'lr'

upload_file = {
	"parameters": [
		{
			"name": "origin",
			"in": "formData",
			"type": "file",
			"required": 'false'
		},
		{
			"name": "comparer",
			"in": "formData",
			"type": "file",
			"required": 'false'
		}
	],
	"responses": {
		"200": {
			"description": "上传文件成功",
			"examples": {}
		}
	}
}

download_file = {
	"parameters": [
		{
			"file_name": "",
			"in": "path",
			"type": "string",
			"enum": ['Python面向对象编程指南.epub'],
			"default": 'Python面向对象编程指南.epub',
			"required": 'true'
		},
	],
	"responses": {
		"200": {
			"description": "下载文件成功",
			"examples": {}
		}
	}
}