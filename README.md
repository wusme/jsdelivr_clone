
Autocard 
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
 
依赖proxy_pool, 必须配置完毕并开启，方法见[proxy_pool](https://github.com/jhao104/proxy_pool)。  
## 用法
```shell
python jc.py github仓库链接(不带.git) 下载文件夹
```
## usage
```shell
python jc.py github_repo(without '.git') download_dir
```
