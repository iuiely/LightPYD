# !/usr/bin/env python
#coding:utf-8
# python模拟linux的守护进程
import os
import sys
import time
import atexit
import string 
import ctypes
import setproctitle
from signal import SIGTERM
from apps.console import *

#libc=ctypes.CDLL('libc.so.6')

class Daemonize() :
    def __init__(self, config):
#        print(config)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if config['pid_file'] != '':
            self.pid_file = config['pid_file']
        else :
            self.pid_file = BASE_DIR+'/runtime/pid/'+config['service']+'.pid'
        if config['access_log'] != '':
            self.access_log = config['access_log']
        else :
            self.access_log = BASE_DIR+'/logs/'+config['service']+'/access.log'
        if config['error_log'] != '':
            self.error_log = config['error_log']
        else :
            self.error_log = BASE_DIR+'/logs/'+config['service']+'/error.log'

        if config['service'] != '':
            self.process_name = config['service']
        else :
            self.process_name = 'python-service'

        if config['app_path'] != '':
            self.app_path = config['app_path']
        else :
            self.app_path = 'apps'

        self.classname = config['class']
        self.method = config['method']
        self.stdin  = '/dev/null'
        self.stdout = self.access_log
        self.stderr = self.error_log
        self._debug = False
        
    # 获取当前是否是调试模式
    @property
    def DebugMode(self):
        return self._debug
 
    # 调试模式开关，默认不是调试模式
    @DebugMode.setter
    def DebugMode(self, DebugMode):
        self._debug = DebugMode
 
    # 调试模式和非调试模式设置
    def _verbosSwitch(self):
        # 调试模式
        if self._debug:
            pass
        else:
            self.stdin = '/dev/null'
            self.stdout = '/dev/null'
            self.stderr = '/dev/null'

    def _daemonize(self):
        #libc = ctypes.CDLL('libc.so.6')
        #libc.prctl(15,self.process_name)
        try:
            # 生成子进程，脱离父进程
            pid = os.fork()
            if pid > 0:
                # 退出父进程，系统的init将会接管子进程
                sys.exit(0)
        except OSError:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)
        # 修改进程工作目录
        os.chdir("/") 
        # 设置新的会话
        os.setsid()  
        # 设置工作目录的umask
        os.umask(0) 
 
        try:
            # 第二次fork，子进程派生一个子进程
            pid = os.fork()
            if pid > 0:
                # 子进程退出，孙子进程由init进程接管
                sys.exit(0)
        except OSError:
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)
        setproctitle.setproctitle(self.process_name)
        # 把之前的刷到硬盘上
        sys.stdout.flush()
        sys.stderr.flush()
        #设置守护进程名称
        # 重定向标准文件描述符, 把stdout ,stderr 输出到默认或者指定的文件
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
 
        # 注册退出函数，根据文件pid判断是否存在进程
        atexit.register(os.remove, self.pid_file)
        pid = str(os.getpid())
        open(self.pid_file, 'w+').write('%s\n' % pid)

    # 设置工作
    def run_task(self,classname,method):
        im_obj = self.app_path+'.'+classname
        im_cls = __import__(im_obj,fromlist=('*'))
        _class = getattr(im_cls,classname)
        obj = _class()
        mtd = getattr(obj,method)
        mtd()
        # 工作内容
        '''
        while True:
            # print '%s:hello world\n' % (time.ctime(),)
            sys.stdout.write('%s:hello world\n' % (time.ctime(),))
            sys.stdout.flush()
            time.sleep(2)
        '''

    # 获取PID
    def get_pid(self):
        try:
            # 读取保存PID的文件
            fp= open(self.pid_file, 'r')
            pid = int(fp.read().strip())
            fp.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid

    def start(self, *args, **kwargs):
        # 检查pid是否存
        try:
            pid = self.get_pid()
        except IOError:
            pid = None
        # 如果PID存在，则说明进程没有关闭。
        if pid:
            message = 'pid_file %s already exist. Process already running!\n'
            sys.stderr.write(message % self.pid_file)
            sys.exit(1)
 
        # 启动守护进程
        self._daemonize()
        # 执行任务
        self.run_task(self.classname,self.method)
 
    def stop(self):
        # 检查pid是否存
        try:
            pid = self.get_pid()
        except IOError:
            pid = None
        if not pid:
            message = 'pid_file %s does not exist. Process not running!\n'
            sys.stderr.write(message % self.pid_file)
            return
        # 杀进程
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
                message = 'Process is stopped.\n'
                sys.stderr.write(message)
        except OSError as err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(self.pid_file):
                    os.remove(self.pid_file)
            else:
                print(str(err))
                sys.exit(1)
    # 重启
    def restart(self, *args, **kwargs):
        self.stop()
        self.start(*args, **kwargs)
 
    # 获取守护程序运行状态
    def status(self):
        try:
            pid = self.get_pid()
        except IOError:
            pid = None
 
        if not pid:
            message = "No such a process running.\n"
            sys.stderr.write(message)
        else:
            message = "The process is running, PID is %s .\n"
            sys.stderr.write(message % str(pid))
        
'''            
if __name__=="__main__":
    config = {'pid_file': '', 'error_log': '', 'access_log': '', 'service': 'vnet-agent', 'class': 'console', 'method': 'execute', 'app_path': '', 'command': ['start']}
    daemon = Daemon(config)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print 'unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart|status' % sys.argv[0]
        sys.exit(2)
'''
