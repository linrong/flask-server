#### Pipenv

##### 什么是Pipenv
[Pipenv](https://docs.pipenv.org/en/latest/)是Kenneth Reitz在2017年1月发布的Python依赖管理工具，现在由PyPA维护。你可以把它看做是pip和virtualenv的组合体，而它基于的[Pipfile](https://github.com/pypa/pipfile)则用来替代旧的依赖记录方式（requirements.txt）。

##### 为什么使用Pipenv
Pipenv会自动帮你管理虚拟环境和依赖文件，并且提供了一系列命令和选项来帮助你实现各种依赖和环境管理相关的操作。简而言之，它更方便、完善和安全。你可以通过[Pipenv文档](https://docs.pipenv.org/en/latest/)开头的介绍来了解它的详细特性。Pipenv的slogan是“Python Dev Workflow for Humans”，作为人类，当然应该尝试一下……

##### 如何使用Pipenv
* 安装
```bash
pip install pipenv
```
* 创建虚拟环境
```bash
# 会在文件夹下生成两个新文件Pipfile和Pipfile.lock
pipenv install
```
* 激活虚拟环境
```bash
pipenv shell
```
* 安装依赖到虚拟环境
```bash
# pipenv区分你是在给哪个虚拟环境工作，依赖的是Pipfile文件的位置
# 1.如果当前目录下不存在Pipfile文件会生成新的虚拟环境
# 2.如果当前目录下存在Pipfile文件会使用已有的Pipfile和Pipfile.lock文件中的配置创建一个虚拟环境
# 3.如果后面带诸如django这一类库名，表示为当前虚拟环境安装第三方库
pipenv install flask
```
* 管理开发环境
```bash
# 通常有一些Python包只在你的开发环境中需要，而不是在生产环境中，例如单元测试包。 Pipenv使用--dev标志区分两个环境
pipenv install --dev django
# django库现在将只在开发虚拟环境中使用。如果你要在你的生产环境中安装你的项目：
pipenv install
# 这不会安装django包
```
* 在虚拟环境中运行命令
```bash
# 使用run参数，提供要运行的命令：
pipenv run python manage.py runserver
# 这将使用当前虚拟环境关联的Python解释器，执行命令。或者简单的执行脚本：
pipenv run python your_script.py
# 如果你不想每次运行Python时都输入这么多字符，可以在shell中设置一个别名，例如:
alias prp="pipenv run python"
prp your_script.py
```
* 冻结Pipfile
```bash
# 冻结就相当于将项目所使用的第三方库列表进行打包输出，类似于virtualenv中生成requirements.txt文件。
# 通过更新Pipfile.lock来冻结库名称及其版本，以及其依赖关系的列表。需要使用lock参数：
pipenv lock
# 冻结之后，如果另一个用户拷贝了你的项目，他们只需要安装Pipenv，然后：
pipenv install
# Pipenv会在项目文件夹下自动寻找Pipfile和Pipfile.lock文件，创建一个新的虚拟环境并安装必要的软件包。
```

* 更换源
```bash
# 1.在Pipfile中更换对应的url即可,如
[[source]]

url = "https://mirrors.aliyun.com/pypi/simple"
verify_ssl = true
name = "pypi"

# 2.
pipenv install --pypi-mirror https://mirrors.aliyun.com/pypi/simple
```

* pipenv 具有的选项
```bash
$ pipenv
Usage: pipenv [OPTIONS] COMMAND [ARGS]...

Options:
  --update         更新Pipenv & pip
  --where          显示项目文件所在路径
  --venv           显示虚拟环境实际文件所在路径
  --py             显示虚拟环境Python解释器所在路径
  --envs           显示虚拟环境的选项变量
  --rm             删除虚拟环境
  --bare           最小化输出
  --completion     完整输出
  --man            显示帮助页面
  --three / --two  使用Python 3/2创建虚拟环境（注意本机已安装的Python版本）
  --python TEXT    指定某个Python版本作为虚拟环境的安装源
  --site-packages  附带安装原Python解释器中的第三方库
  --jumbotron      An easter egg, effectively.
  --version        版本信息
  -h, --help       帮助信息
```
* pipenv 可使用的命令参数：
```bash
Commands:
  check      检查安全漏洞
  graph      显示当前依赖关系图信息
  install    安装虚拟环境或者第三方库
  lock       锁定并生成Pipfile.lock文件
  open       在编辑器中查看一个库
  run        在虚拟环境中运行命令
  shell      进入虚拟环境
  uninstall  卸载一个库
  update     卸载当前所有的包，并安装它们的最新版本
```
* 使用例子
```bash
Usage Examples:
   Create a new project using Python 3.6, specifically:
   使用Python 3.6创建虚拟环境:
   $ pipenv --python 3.6

   Install all dependencies for a project (including dev):
   安装包括开发环境中的第三方库:
   $ pipenv install --dev

   Create a lockfile containing pre-releases:
   $ pipenv lock --pre

   Show a graph of your installed dependencies:
   $ pipenv graph

   Check your installed dependencies for security vulnerabilities:
   $ pipenv check

   Install a local setup.py into your virtual environment/Pipfile:
   $ pipenv install -e .

   Use a lower-level pip command:
   $ pipenv run pip freeze
```



