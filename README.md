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
#### 参考
* [深入Python Flask构建Restful API 或者 慕课网 Python Flask构建可扩展的 ESTful API](https://www.os4team.cn/)
* [labike.github.io](https://github.com/labike/labike.github.io/issues/45)
* [mini-shop-server](https://github.com/Allen7D/mini-shop-server)
* [flask-restful-example](https://github.com/qzq1111/flask-restful-example)