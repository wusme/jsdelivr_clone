
jsdelivr_clone 
========
[![](https://img.shields.io/badge/Powered%20by-Requests-green.svg)](http://www.python-requests.org)
[![](https://img.shields.io/badge/language-Python-green.svg)](https://www.python.org)   
> Download github repo with jsdelivr cdn.   
### 下载安装

* 下载源码:

```shell
git clone git@github.com:Ghosin/jsdelivr_clone.git

或者直接到https://github.com/Ghosin/jsdelivr_clone 下载zip文件
```

* 安装依赖:

```shell
pip install -r requirements.txt
```
* 创建OAuth Apps，将client_id和client_secret填入config.py
```Python
client_id = 'client_id'
client_secret = 'client_secret'
```
## 用法
```shell
python jc.py github仓库链接(不带.git) 下载文件夹
```
