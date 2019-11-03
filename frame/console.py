import os
import sys
from frame.lib.ConsoleServer import *
class console :
    
    @classmethod
    def run(cls,config):
        command = config['command']
        if len(command) == 1 and command[0] == 'help' :
            cls().help()
        elif len(command) == 1 and command[0] == 'start' :
            cls().start(config)
        elif len(command) == 2 and command[0] == 'start' and command[1] == '-d':
            cls().start_d(config)
        elif len(command) == 1 and command[0] == 'stop':
            cls().stop(config)
        elif len(command) == 1 and command[0] == 'status':
            cls().status(config)
        elif len(command) == 1 and command[0] == 'restart':
            cls().restart(config)
        else :
            cls().help()

    @classmethod
    def help(self):
        print('You need input : start|stop|restart|status|help')

    @classmethod
    def start(self,config):
        ConsoleServer.start(config)

    @classmethod
    def start_d(self,config):
        print(config)

    @classmethod
    def stop(self,config):
        ConsoleServer.stop(config)

    @classmethod
    def restart(self,config):
        print(config)

    @classmethod
    def status(self,config):
        print(config)

