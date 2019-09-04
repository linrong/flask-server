# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/08/30.
"""
from functools import wraps
from flask import request
from werkzeug.contrib.cache import SimpleCache

__author__ = 'lr'

'''
class Limiter(object):
    cache = SimpleCache()

    def limited(self, callback):
        self.limited_callback = callback
        return callback

    def limit(self, key='', key_func=None, time_delta=60):
        def decorator(f):
            key_prefix = "limiter/"

            @wraps(f)
            def wrapper(*args, **kwargs):
                # global cache
                full_key = key_prefix + key_func() if key_func else key
                value = Limiter.cache.get(full_key)
                if not value:
                    Limiter.cache.set(full_key, time_delta, timeout=time_delta)
                    return f(*args, **kwargs)
                else:
                    return self.limited_callback()

            return wrapper

        return decorator
'''

cache = SimpleCache()

def cached(timeout=5 * 60, key='cached_{}_{}'):
    '''
	:param timeout: 缓存的秒数
	:param key: 缓存的key的格式
	:return:
	'''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
			# 以 { key:value } 的形式存到内存
            query_args = dict(request.args.to_dict())
            body_args = request.get_json(silent=True) or {}
            req_args = {**query_args, **body_args}
            suffix = ''
            for (k, v) in req_args.items():
                suffix = suffix + '&{}={}'.format(k, v)
            cache_key = key.format(request.path, suffix)
            value = cache.get(cache_key)  # 获取
            if value is None:
                value = f(*args, **kwargs)
                cache.set(cache_key, value, timeout=timeout)  # 设置
            return value
        return decorated_function
    return decorator