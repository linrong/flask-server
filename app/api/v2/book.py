# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from sqlalchemy import or_

from app.libs.success_code import Success
from app.libs.redprint import RedPrint
from app.models.book import Book
from app.validators.forms import BookSearchValidator

__author__ = 'lr'

api = RedPrint('book')

@api.route('/search', methods=['GET'])
def search():
    form = BookSearchValidator().validate_for_api()
    q = '%' + form.q.data + '%'
    books = Book.query.filter(
        or_(Book.title.like(q), Book.publisher.like(q))).all() # 模糊查询
    books = [book.hide('summary') for book in books] # 隐藏字段
    return Success(books)


@api.route('/<isbn>/detail', methods=['GET'])
def detail(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    return Success(book)
