import os
from sys import version_info
if version_info.major == 2 and version_info.minor ==7:
    import ConfigParser
    configparser = ConfigParser.ConfigParser()
elif version_info.major == 3 :
    import configparser
    configparser = configparser.ConfigParser()


class Config(object):

    cfg_dict = {}

    def __init__(self):
        self.cfg=None

    @classmethod
    def DictMake(cls,_file):
        if os.access(_file, os.R_OK) :
            conf =_file

        cls.cfg = configparser
        cls.cfg.read(conf)
        #section = cfg.sections();
        for section in cls.cfg.sections():
            for key in cls.cfg.options(section) :
                cls.cfg_dict[key] = cls.cfg.get(section,key)
                
        return cls.cfg_dict

'''
if __name__ =='__main__':
    _file = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))+'/frame/config.ini'
    print(_file)
    #config = Config()
    res = Config.DictMake(_file)
    print(res)
'''
