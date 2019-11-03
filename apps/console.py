#coding=  utf-8
import os
import sys
import time

class console(object) :
    def execute(self) :
        # 工作内容
        while True:
        # print '%s:hello world\n' % (time.ctime(),)
            sys.stdout.write('%s:hello world\n' % (time.ctime(),))
            sys.stdout.flush()
            time.sleep(2)
