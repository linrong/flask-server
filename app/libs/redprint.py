# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
__author__ = 'lr'

# 创建自定义红图对象


class RedPrint:

	"""
	初始化传入视图名name
	mount是一个存放多个视图函数的列表
	"""
    def __init__(self, name):
        self.name = name
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
            endpoint = self.name + '+' + options.pop("endpoint", f.__name__)
            # 将视图函数注册到蓝图上来
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
