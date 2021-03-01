# -- encoding: utf-8 --
# @time:    2020/12/5 19:18
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: yamlhandler2.py
import datetime
import os
from sys import path

import yaml
# pip install pyyaml
class DLYaml:
    env = {
        "default": "test",
        "testing-studio":
        {
        "dev":"127.0.0.1",
         "test":"127.0.0.2"
        }
    }
    def dump_yaml(self):
        # 生成现在的时间
        # t = datetime.datetime.now()
        # 对现在时间格式化，以此作为文件名
        # file_name = os.path.join(path+t.strftime('%Y%m%d %H:%M:%S')+'.yaml')
        # os.mkdir(file_name)
        file_name = 'env.yaml'
        with open(file_name,'w') as f:
            yaml.safe_dump(data=self.env,stream=f)
    def load_yaml(self,file_name):
        res = yaml.safe_load(open(file_name))
        return res
if __name__ == '__main__':
    DLYaml().dump_yaml()
    # data = DLYaml().load_yaml()
    # print(data)