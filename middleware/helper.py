# -- encoding: utf-8 --
# @time:    2020/12/6 23:34
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: helper.py
import json
import re

from common.myslqhandler import MysqlHandler
from common.requesthandler import RequestHandler
from config.settings import dev_settings
from middleware.get_yaml_data import yaml_data
from jsonpath import jsonpath
import random
from middleware.db_handler import DBHandler


def admin_login():
    json_data = RequestHandler().request_handler(method=yaml_data['admin_login']['method'],
                                                 url=(dev_settings.host + yaml_data['admin_login']['url']),
                                                 json=yaml_data['admin_login']['data'],
                                                 headers=yaml_data['admin_login']['headers'])
    return json_data


def login():
    json_data = RequestHandler().request_handler(method=yaml_data['login']['method'],
                                                 url=(dev_settings.host + yaml_data['login']['url']),
                                                 json=yaml_data['login']['data'],
                                                 headers=yaml_data['login']['headers'])
    return json_data


def save_admin_token():
    json_data = admin_login()
    admin_member_id = jsonpath(json_data, '$..id')[0]
    token_type = jsonpath(json_data, '$..token_type')[0]
    token = jsonpath(json_data, '$..token')[0]
    admin_Authorization = " ".join([token_type, token])

    Context.admin_Authorization = admin_Authorization
    Context.admin_member_id = admin_member_id


def save_token():
    json_data = login()
    member_id = jsonpath(json_data, '$..id')[0]
    token_type = jsonpath(json_data, '$..token_type')[0]
    token = jsonpath(json_data, '$..token')[0]
    Authorization = " ".join([token_type, token])

    Context.Authorization = Authorization
    Context.member_id = member_id


class Context:
    Authorization = ''
    member_id = None
    loan_id = None

    admin_Authorization = ''
    admin_member_id = None
    add_loan_id = None

    mobile_phone = "13712341235"
    pwd = "12345678"
    admin_mobile_phone = "18593298080"
    admin_pwd = "12345678"


def generate_member_id():
    # 生成数据库中不存在的用户id
    member_id = random.randint(100000, 999999)
    return member_id


def generate_nick_name():
    nick_name = 'json'
    n = random.choice(range(1, 6))
    for i in range(n):
        end = random.randint(0, 9)
        nick_name += str(end)
    return nick_name


def generate_ten_nick_name():
    ten_nick_name = 'json'
    for i in range(5):
        end = random.randint(0, 9)
        ten_nick_name += str(end)
    return ten_nick_name


def generate_add_loan_id():
    add_loan_id = random.randint(100000, 1000000)
    return add_loan_id


def save_loan_id():
    MH = MysqlHandler(host=yaml_data['database']['host'],
                      port=yaml_data['database']['port'],
                      user=yaml_data['database']['user'],
                      password=yaml_data['database']['password'],
                      database=yaml_data['database']['database'],
                      charset=yaml_data['database']['charset'])
    sql = "SELECT * from loan WHERE status=2 limit 1;"
    loan_id = MH.select_sql(sql=sql)["id"]
    Context.loan_id = loan_id


def save_added_id():
    MH = MysqlHandler(host=yaml_data['database']['host'],
                      port=yaml_data['database']['port'],
                      user=yaml_data['database']['user'],
                      password=yaml_data['database']['password'],
                      database=yaml_data['database']['database'],
                      charset=yaml_data['database']['charset'])
    sql = "SELECT * from loan WHERE status=1 limit 1;"
    added_loan_id = MH.select_sql(sql=sql)["id"]
    Context.add_loan_id = added_loan_id


def replace_label(target):
    global new_str
    re_pattern = r"#(.*?)#"
    while re.findall(re_pattern, target):
        key = re.search(re_pattern, target).group(1)
        new_str = re.sub(re_pattern, str(getattr(Context, key)), target, 1)
    return new_str


if __name__ == '__main__':
    # save_token()
    # print(Context.member_id)
    # print(Context().Authorization)

    # member_id = generate_member_id()
    # print(member_id)

    # save_loan_id()
    # print(Context.loan_id)

    # target = r'{"member_id":"#member_id#","loan_id":"#loan_id#","token":"#token#","username":"#username#"}'
    # print(replace_label(target))

    # json_data = login()
    # print(json_data)

    nick_name = generate_nick_name()
    print(nick_name)

    ten_nick_name = generate_ten_nick_name()
    print(ten_nick_name)
