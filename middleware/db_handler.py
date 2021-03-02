# -- encoding: utf-8 --
# @time:    2020/12/13 23:48
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: db_handler.py
from common.myslqhandler import MysqlHandler
from middleware.get_yaml_data import yaml_data
class DBHandler(MysqlHandler):
    def __init__(self):
        super().__init__(host=yaml_data['database']['host'],
                          port=yaml_data['database']['port'],
                          user=yaml_data['database']['user'],
                          password=yaml_data['database']['password'],
                          database=yaml_data['database']['database'],
                          charset=yaml_data['database']['charset'])

