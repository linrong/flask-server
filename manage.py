# _*_ coding: utf-8 _*_
"""
  Created by lr on 2019/8/9.
"""
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError
from app.models.base import db

__author__ = 'lr'

app = create_app()

# 拦截全局异常处理
@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    elif isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(code, error_code, msg)
    else:
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e

# http://docs.jinkan.org/docs/flask/deploying/wsgi-standalone.html#deploying-proxy-setups
app.wsgi_app = ProxyFix(app.wsgi_app)

manager = Manager(app)
manager.add_command("run", Server())
manager.add_command("runserver", Server(
    use_debugger=True, use_reloader=True,
    host='0.0.0.0', port=8010
))

# 要使用flask-migrate，必须先绑定db和app
migrate = Migrate(app, db)
# 将MigrateCommand添加到manager中，"db"是自定义命令
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
