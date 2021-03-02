# -- encoding: utf-8 --
# @time:    2020/12/5 14:22
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: loggerhandler.py
import logging
from logging import Logger
import os
from config.settings import  dev_settings

class LoggerHandler(Logger):
    def __init__(self,
                 name='py_api_test',
                 level = 'DEBUG',
                 FileHandler_level = 'WARNING',
                 console_level = 'INFO',
                 format = '%(asctime)s-%(filename)s-%(lineno)d-%(name)s-%(levelname)s-日志信息:%(message)s',
                 file = None):
        # 初始化收集器
        # logger = logging.getLogger(name)
        super().__init__(name)
        # 设置收集器级别
        self.setLevel(level)
        # 设置日志格式
        formatter = logging.Formatter(format)
        # 初始化处理器
        if file:
            fh = logging.FileHandler(file,encoding='UTF-8')
            # 设置handler级别
            fh.setLevel(FileHandler_level)
            # 设置处理器输出格式 file_handler.setFormatter(fmt)
            fh.setFormatter(formatter)
            # 添加处理器 addHandler
            self.addHandler(fh)
        ch = logging.StreamHandler()
        ch.setLevel(console_level)
        ch.setFormatter(formatter)
        self.addHandler(ch)

# parent_path = os.path.dirname(os.path.abspath(__file__))
# logs_path = os.path.join(parent_path,'logs')

base_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
# print(base_path)
log_path = dev_settings.log_path
if not os.path.exists(log_path):
     os.mkdir(log_path)
file_name = 'api_test_log.txt'
logs_file = os.path.join(log_path,file_name)

logger = LoggerHandler(file=logs_file)
# logger = LoggerHandler2(name=config.logger_name,file=config.logger_file)

if __name__ == '__main__':
    logger = LoggerHandler()
    info_msg = 'info级别信息'
    error_msg = 'error错误信息'
    logger.error(error_msg)
    logger.info(info_msg)