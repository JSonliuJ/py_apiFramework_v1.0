# -- encoding: utf-8 --
# @time:    2020/12/6 23:51
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: get_yaml_data.py
from common.yamlhandler import YamlHandler
from config.settings import dev_settings
yaml_data = YamlHandler(dev_settings.conf_yaml_path).read_yaml()