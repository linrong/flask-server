# flask-server
this is a project for flask server

#### 开发
基于vscode+remote container 或者remote ssh

* 在remote container 安装python插件

* 安装pipenv
```bash
pip install pipenv -i https://mirrors.aliyun.com/pypi/simple
```
* 安装库
```bash
# 创建虚拟环境
pipenv install --pypi-mirror https://mirrors.aliyun.com/pypi/simple

# 修改pipfile
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]

[requires]
python_version = "3.7"
# 为
[[source]]
name = "pypi"
url = "https://mirrors.aliyun.com/pypi/simple"
verify_ssl = true

[dev-packages]

[packages]

[requires]
python_version = "3.7"

# 安装库
pipenv install flask
```
#### 运行
```bash
# 使用docker-compose.yml方式运行
# 端口映射8010，访问本机地址8010即可
```

#### 模块
> 主要按照在使用的技术中占多大比例划分
* 视图(包括自定义红图和蓝图)
* 配置
* 数据(异常处理，数据的序列化，数据的检查)
* 访问认证和权限划分
* model和orm
* flask

#### 参考
* [深入Python Flask构建Restful API 或者 慕课网 Python Flask构建可扩展的 ESTful API](https://www.os4team.cn/)
* [labike.github.io](https://github.com/labike/labike.github.io/issues/45)
* [mini-shop-server](https://github.com/Allen7D/mini-shop-server)
* [flask-restful-example](https://github.com/qzq1111/flask-restful-example)