# -- encoding: utf-8 --
# @time:    2020/12/5 14:27
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: confhandler.py
from configparser import ConfigParser
class ConfigHandler(ConfigParser):
    def __init__(self,file,encoding='utf-8'):
        # config =  ConfigParser()
        super().__init__()
        self.read(file, encoding=encoding)

if __name__ == '__main__':
    pass
