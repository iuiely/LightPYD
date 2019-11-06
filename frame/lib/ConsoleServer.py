import os
import sys
from frame.lib.Daemonize import *

class ConsoleServer :
    @classmethod
    def start(cls,config) :
        daemonize = Daemonize(config)
        daemonize.start()

    @classmethod
    def stop(cls,config):
        daemonize = Daemonize(config)
        daemonize.stop()
    @classmethod
    def restart(cls,config):
        print(config)
    @classmethod
    def status(cls,config):
        print(config)
