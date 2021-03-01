# -- encoding: utf-8 --
# @time:    2020/12/13 0:21
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: regxhandler.py
import re


class RegxHandler:
    def universal_regx_handler(self, custom_pattern, str):
        data = re.search(custom_pattern, str)
        return data

    def str_substitute(self, custom_pattern, new, str, count=1):
        new_str = re.sub(custom_pattern, new, str, count=count)
        return new_str

    def match_qq(self, str):
        # re.compile()将正则表达式编译成Pattern对象
        pattern = re.compile(r'[1-9][0-9]{4,10}')
        return re.search(pattern, str)

    def match_mobile_phone(self, str):
        pattern = re.compile(r'1[35789]\d{9}')
        return re.search(pattern, str)

    def match_email(self, str):
        pattern = re.compile(r'\w{5,20}@(163|126|qq|139)\.(com|cn)')
        return re.search(pattern, str)

    def match_username(self, str):
        pattern = re.compile(r'[a-zA-Z_0-9]{5,20}')
        # pattern = re.compile(r'\w{5,20}')
        return re.search(pattern, str)

    def match_domain_name(self, str):
        # 匹配域名
        pattern = re.compile(r'[a-zA-Z]+://[^\s]*[.com|.cn]')
        return re.search(pattern, str)


if __name__ == '__main__':
    regx = RegxHandler()
    # str = 'abJsonabcAbc'
    # custom_pattern = 'abc'
    # data = regx.universal_regx_handler(custom_pattern,str)
    # print(data)
    qq = 'aaf810038888881100bbn'
    data = regx.match_qq(qq)
    print(data)

    str = "[jfjaognag.jpg] http://map.baidu.com http:www.runoob.com"
    res = regx.match_domain_name(str=str)
    print(res)
