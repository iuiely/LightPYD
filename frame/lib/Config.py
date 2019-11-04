import os,sys,pdb
from sys import version_info
if version_info.major == 2 and version_info.minor ==7:
    import ConfigParser
    configparser = ConfigParser.ConfigParser()
elif version_info.major == 3 :
    import configparser
    configparser = configparser.ConfigParser()

class Config(object):
    def __init__(self):
        self.cfg=None
    @classmethod
    def DictMake(cls,_file,path=None):
        cls.cfg_dict ={}
        if path is None:
            if os.access(_file, os.R_OK) :
                conf =_file
        else:
            if os.access(path+_file,os.R_OK):
                conf = path+'/'+_file
        cls.cfg = configparser
        for a in cls.cfg.sections() :
            cls.cfg.remove_section(a)
        cls.cfg.read(conf)
        for section in cls.cfg.sections():
            for key in cls.cfg.options(section) :
                cls.cfg_dict[key] = cls.cfg.get(section,key)
        return cls.cfg_dict

    @classmethod
    def get(cls,name,path=None):
        cls.cfg_dict ={}
        if name is None :
            return False
        _name = name.split('.')
        num = len(_name)
        if num == 1 :
            _name = name.lower()
            if path is None:
                path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                _file = path+'/config/'+_name+'.ini'
            else:
                _file = path+'/'+_name+'.ini'
            if os.path.exists(_file) == False:
                return False
            cls.cfg = configparser
            for a in cls.cfg.sections() :
                cls.cfg.remove_section(a)
            cls.cfg.read(_file)
            for section in cls.cfg.sections():
                for key in cls.cfg.options(section) :
                    cls.cfg_dict[key] = cls.cfg.get(section,key)
            return cls.cfg_dict
        else:
            _file_prefix = _name.pop(0).lower()
            if path is None:
                path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                _file = path+'/config/'+_file_prefix+'.ini'
            else:
                _file = path+'/'+_file_prefix+'.ini'
            if os.path.exists(_file) == False:
                return False
            cls.cfg = configparser
            cls.cfg.read(_file)
            section = _name.pop(0)
            if len(_name) == 0:
                return dict(cls.cfg.items(section))
            else:
                key=_name.pop(0)
                return cls.cfg.get(section,key)
