# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/29.
  可以用来处理上传产品图片、Excel等
"""
import os
from flask import request, current_app
from flask import send_from_directory

from app.libs.redprint import RedPrint
from app.libs.success_code import Success, RenewSuccess
from app.validators.forms import UploadPDFValidator

__author__ = 'lr'


api = RedPrint(name='file', description='文件上传')

@api.route('/upload', methods=['POST'])
@api.doc()
def upload_file():
    '''文件上传'''
    form = UploadPDFValidator().validate_for_api()
    origin_file = request.files[form.origin.name]
    origin_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], origin_file.filename))
    comparer_file = request.files[form.comparer.name]
    comparer_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], comparer_file.filename))
    return RenewSuccess()

@api.route('/download/<string:file_name>', methods=['GET'])
@api.doc()
def download_file(file_name):
	'''文件下载'''
	print('file_name', file_name)
	return Success(file_name)
	# return send_from_directory(file_name, file_name, mimetype='application/octet-stream')