# LightPYD
  一个轻量级的,基于python fork 的守护进程框架，支持通过简单的配置，把任务变成守护进程，支持日志和守护进程改名，目前版本V0.1 <br>
  (A lightweight python daemon framework)
## 框架定位
  使用python语言，想把周期性任务以后台守护进程的运行的开发者和使用者
## 环境要求
  python2.7 or python3.6 <br>
  linux <br>
## 快速使用
##### 创建目录
  mkdir /opt/python-daemonize <br>
  cd /opt/python-daemonize <br>
##### 下载框架
  git clone https://github.com/iuiely/LightPYD.git <br>
##### 守护进程模式启动
  /opt/python-daemonize/LightPYD {app} start  <br>
  {app} 是应用配置文件的名称 <br>
  例如:配置文件的名称是 system, 启动命令是：/opt/python-daemonize/LightPYD system start <br>
##### 守护进程模式停止
  /opt/python-daemonize/LightPYD {app} stop  <br>
  {app} 是应用配置文件的名称 <br>
  例如:配置文件的名称是 system, 停止命令是：/opt/python-daemonize/LightPYD system stop <br>
##### 简单测试
  测试启动 <br>
  /opt/python-daemonize/LightPYD config start <br>
  测试代码 <br>
  /opt/python-daemonize/apps/console.py
```
#coding=  utf-8
import os
import sys
import time

class console(object) :
    def execute(self) :
        # content
        while True:
        # print '%s:hello world\n' % (time.ctime(),)
            sys.stdout.write('%s:hello world\n' % (time.ctime(),))
            sys.stdout.flush()
            time.sleep(2)
```
  查看日志 cat /opt/python-daemonize/logs/LightPYD/access.log
```
Sun Nov  3 12:02:15 2019:hello world
Sun Nov  3 12:02:17 2019:hello world
Sun Nov  3 12:02:19 2019:hello world
```
  测试停止 <br>
  /opt/python-daemonize/LightPYD config stop
## 开发文档
### 主要文件说明
##### 守护进程的启动脚本
  bin/LightPYD <br>
##### 守护进程配置文件和格式
  frame/config.ini <br>
  这个文件存放守护进程的各项配置，只和守护进程相关，格式如下 <br>
```
[default]
# 应用的 pid 存储位置
pid_file = 
#应用的 stderr 存储位置
error_log = 
#应用的 stdout 存储位置
access_log = 
#应用的 守护进程名称
service = LightPYD
[server]
# 运行在守护进程下的应用的主类名
class = console
# 运行在守护进程下的应用的方法名
method = execute
# 运行在守护进程下的应用的目录,空表示子目录apps,示例格式:apps.system
app_path =
```
##### 应用配置文件和格式
  config/LightPYD.ini <br>
  这个配置文件存放应用的各项配置，最好只和应用本身相关。例如mysql,redis,rabbitmq等等，格式如下
```
[default]
my_ip = 192.168.1.102
[mysql]
mysql_connection = mysql+pymysql://db_user:db_password@db_host:db_port/db_database
```
