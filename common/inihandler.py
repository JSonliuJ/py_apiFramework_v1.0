# -- encoding: utf-8 --
# @time:    2020/12/5 14:29
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: inihandler.py
from configparser import ConfigParser
class IniHandler:

    @staticmethod
    def ini_read(file,section,option):
        cf = ConfigParser()
        cf.read(file, encoding='utf-8')
        return cf[section][option]

    def ini_write(self,file):
        cf = ConfigParser()
        with open(file,'a',encoding='utf-8') as f:
            cf.write(f)
if __name__ == '__main__':
    pass