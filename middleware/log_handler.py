# -- encoding: utf-8 --
# @time:    2020/12/13 23:49
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: log_handler.py
import os
from config.settings import dev_settings
from middleware.get_yaml_data import yaml_data
from common.loggerhandler import LoggerHandler
log_file = os.path.join(dev_settings.log_path,yaml_data['logger']['file'])

class LogHandler(LoggerHandler):
    def __init__(self):
        super().__init__(name=yaml_data['logger']['name'],
                       level=yaml_data['logger']['level'],
                       FileHandler_level=yaml_data['logger']['FileHandler_level'],
                       console_level=yaml_data['logger']['console_level'],
                       format='%(asctime)s-%(filename)s-%(lineno)d-%(name)s-%(levelname)s-日志信息:%(message)s',
                       file=log_file)

logger = LogHandler()