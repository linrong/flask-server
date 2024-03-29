# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""

from contextlib import contextmanager
from datetime import datetime
from flask import current_app, json
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, Pagination as _Pagination, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer, orm, inspect
from time import localtime, strftime

from app.libs.error_code import NotFound

__author__ = 'lr'


"""
没有使用@contextmanager时应该操作数据库的方式
try:
	user_db = User(email=self.email, nickname=self.nickname, password=self.password)
	db.session.add(user_db)
	#所有的数据处理准备好之后，执行commit才会提交到数据库
	db.session.commit()
except Exception as e:
	#加入数据库commit提交失败，必须回滚
	db.session.rollback()
	raise e
"""
# 自定义一个SQLAlchemy继承flask_sqlalchemy的,方便自定义方法
class SQLAlchemy(_SQLAlchemy):
	# 利用contextmanager管理器,对try/except语句封装，使用的时候必须和with结合
	# 调用时使用with调用,会先执行auto_commit到yield停止，执行with代码，如何再执行yield下面的
	@contextmanager
	def auto_commit(self):
		try:
			yield
			self.session.commit()  # 事务
		except Exception as e:
			self.session.rollback()  # 回滚
			raise e

	@contextmanager
	def auto_check_empty(self, e):
		try:
			yield
		except Exception:
			raise e

class Pagination(_Pagination):
	def hide(self, *keys):
		for item in self.items:
			item.hide(*keys)
		return self


class Query(BaseQuery):
	# 过滤的已经软删除的数据
	def filter_by(self, **kwargs):
		if 'status' not in kwargs.keys():
			kwargs['status'] = 1
		return super(Query, self).filter_by(**kwargs)

    # 数据list化
	def all(self):
		rv = list(self)
		if not rv:
			raise NotFound()
		return rv
		
	def all_or_404(self, e=None, error_code=None, msg=None):
		rv = list(self)
		if not rv:
			if not rv:
				if e:
					raise e
				raise NotFound(error_code=error_code, msg=msg)
		return rv

	def get_or_404(self, ident, e=None, error_code=None, msg=None):
		rv = self.get(ident)  # 查询主键
		if not rv:
			if e:
				raise e
			raise NotFound(error_code=error_code, msg=msg)
		return rv

    # 重写修改错误的返回格式，此方法BaseQuery自带的
	def first_or_404(self, e=None, error_code=None, msg=None):
		'''
		:param e: 异常(exception)
		:param error_code: 错误码
		:param msg: 错误信息
		:return:
		'''
		rv = self.first()
		if not rv:
			if e:
				raise e
			raise NotFound(error_code=error_code, msg=msg)
		return rv

	def paginate(self, page=None, per_page=None, error_out=True, max_per_page=None):
		paginate = BaseQuery.paginate(self, page=page, per_page=per_page, error_out=error_out, max_per_page=max_per_page)
		return Pagination(self,
						  paginate.page,
						  paginate.per_page,
						  paginate.total,
						  paginate.items
						  )

# 实例化SQLAlchemy对象并且重写query_class
# flask里面通过flask_sqlalchemy快速使用SQLAlchemy
# SQLAlchemy是python对于数据库的orm库
db = SQLAlchemy(query_class=Query)

# 创建model的基类
class Base(db.Model):
	# Flask-SQLAlchemy创建table时,如何声明基类（这个类不会创建表,可以被继承）
    # 方法就是把__abstract__这个属性设置为True,这个类为基类，不会被创建为表
	__abstract__ = True
	create_time = Column('create_time', Integer) # 存储int型时间戳 
	delete_time = Column(Integer)
	update_time = Column(Integer)
	status = Column(SmallInteger, default=1)  # 软删除，SmallInteger取值范围小的整数，一般是 16 位
    
	# sqlAlchemy ORM不调用__init__从数据库行重新创建对象时。ORM的过程有点类似于Python标准库的 pickle 模块，调用低级__new__方法，然后在实例上悄悄地恢复属性，而不是调用__init__
	# 如果需要在数据库加载的实例准备好使用之前对其进行一些设置，则存在一个事件挂钩，称为 InstanceEvents.load() 这可以实现；它也可以通过一个特定于类的修饰符调用 orm.reconstructor() . 
	# 使用时 orm.reconstructor() 每次加载或重建类的实例时，映射器都将调用不带参数的修饰方法。这对于重新创建通常在 __init__ 
	# 文档https://docs.sqlalchemy.org/en/13/orm/constructors.html
	# 意思大概是SQLachemy实例化创建对象进行crud时不像python中的类一样会调用__init__，而是使用__new__，如果有需求的可以使用@orm.reconstructor装饰器实现创建对象时调用进行一些初始化操作
	@orm.reconstructor
	def init_on_load(self):
		self.exclude = ['create_time', 'update_time', 'delete_time', 'status']
		# inspect()函数是SQLAlchemy的公共API的入口点，用于查看内存中对象的配置和构造。根据传递给inspect()的对象的类型，返回值可以是提供已知接口的相关对象，或者在许多情况下它将返回对象本身
		all_columns = inspect(self.__class__).columns.keys() # 例如相当于获取到User.colums.keys()
		self.fields = list(set(all_columns) - set(self.exclude)) # 设置self.fields,用于确定每个model要返回什么字段数据，什么字段数据不返回？
		self.hide_fields = [] # 被隐藏的属性则无法用append方法添加

	def __init__(self):
		self.create_time = int(datetime.now().timestamp()) # 存储int型时间戳 
    
	# 用于序列化时使用dict(xxx)方式序列化model
	def __getitem__(self, item):
		attr = getattr(self, item)
		# 将字符串转为JSON
		if isinstance(attr, str):
			try:
				attr = json.loads(attr)
			except ValueError:
				pass
		# 处理时间(时间戳转化)
		if item in ['create_time', 'update_time', 'delete_time']:
			attr = strftime('%Y-%m-%d %H:%M:%S', localtime(attr))
		return attr
    
	# 装饰器，将装饰的方法可以按照属性使用（get,set）
	@property
	def create_datetime(self):
		if self.create_time:
			return datetime.fromtimestamp(self.create_time) # int时间戳转日期格式
		else:
			return None

	def get_url(self, url):
		if (self._from == 1):
			return current_app.config['IMG_PREFIX'] + url
		else:
			return url

	def set_attrs(self, **kwargs):
		# 快速赋值
		# 用法: set_attrs(form.data)
		for key, value in kwargs.items():
			if hasattr(self, key) and key != 'id':
				setattr(self, key, value)

	def delete(self):
		self.status = 0

	def keys(self):
		# 在 app/app.py中的 JSONEncoder中的 dict(o)使用
		# 在此处，整合要输出的属性：self.fields
		return self.fields

	def hide(self, *keys):
		for key in keys:
			self.hide_fields.append(key)
			if key in self.fields:
				self.fields.remove(key)
		return self

	def append(self, *keys):
		for key in keys:
			# self.fields 暂未有key 
			# and
			# 在 Model层和 Service层等任意的操作中，已经隐藏的属性无法再添加
			if key not in self.fields and key not in self.hide_fields:
				self.fields.append(key)
		return self
