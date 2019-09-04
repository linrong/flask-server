# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
__author__ = 'lr'

from functools import wraps
from flasgger import swag_from

from app import api_docs

# 创建自定义红图对象


class RedPrint:

    """
	初始化传入视图名name
	mount是一个存放多个视图函数的列表
	"""
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.mound = []

    """
	这里我们没有办法没有像Flask Blueprint在route内部实现视图函数向Blueprint的注册
	因为我们在Redprint里拿不到Blueprint对象
	所以我们只能暂时将所有参数存储在mount列表中    
	"""
    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f

        return decorator

    """
    register方法就是Redprint向Blueprint注册的方法
    register方法通过一个bp参数, bp就是Blueprint对象
    然后调用Blueprint的add_url_rule实现Redprint向Blueprint的注册
    """
    def register(self, bp, url_prefix=None):
        # 如果不传url_prefix 则默认使用name
        if url_prefix is None:
            url_prefix = '/' + self.name
        # python的自动拆包
        for f, rule, options in self.mound:
            # 将endpoint返回的格式拼装成v1.redprint_name + view_func,在进行权限判断时使用
            endpoint = self.name + '+' + options.pop("endpoint", f.__name__)
            # 将视图函数注册到蓝图上来
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)


    '''
		装饰器执行的顺序(初始化会被执行至 f层；如同洋葱层)
		装饰器到底要的是什么？无非是对函数进行包裹 & 获取函数信息
		对装饰器完善; doc改为swag_from就更好理解
			对于第三方的装饰器，如何「扩张其功能」
			==> 能不能写一个修饰「装饰器」的函数
	'''
    def doc(self, *_args, **_kwargs):
        def decorator(f):
            api_doc = getattr(api_docs, self.name)
            specs = getattr(api_doc, f.__name__)
            specs['tags'] = [self.name]
            # 对f.__doc__处理
            if f.__doc__ and '\n\t' in f.__doc__:
                f.__doc__ = f.__doc__.split('\n\t')[0]

            @swag_from(specs=specs)
            @wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapper

        return decorator

    @property
    def tag(self):
        return {
            'name': self.name,
            'description': self.description
        }
