# -- encoding: utf-8 --
# @time:    2020/12/19 22:53
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: test_005_withdraw_method2.py
import decimal
import json
import os
import unittest
from jsonpath import jsonpath
from lib import ddt
from common.excelhandler import ExcelHandle
from common.requesthandler import RequestHandler
from config.settings import dev_settings
from middleware.get_yaml_data import yaml_data
from middleware import helper
from middleware.helper import save_token
from middleware.log_handler import logger
from middleware.db_handler import DBHandler
@ddt.ddt
class TestWithdrawMethod2(unittest.TestCase):
    EH = ExcelHandle(dev_settings.test_data_path)
    data = EH.read_all_data(yaml_data['excel']['sheet'][6])
    log_file = os.path.join(dev_settings.log_path, yaml_data['logger']['file'])

    def setUp(self):
        # 1. 数据库连接
        self.MH = DBHandler()
        # 2. 请求
        self.req = RequestHandler()

    def tearDown(self):
        # 3. 数据库关闭
        self.MH.close()
        # 4. 会话关闭
        self.req.close_session()

    @ddt.data(*data)
    def test_withdraw_method2(self, test_data):
        global member_id, Authorization
        # 充值第一条用例放已经注册并能成功登陆的手机号用户密码，然后获取token
        # 判断如果是登录成功的接口，获取token的值，self.token = token
        if "login" in test_data["url"]:
            json_data = self.req.request_handler(test_data['method'],
                                                 url=(dev_settings.host + test_data['url']),
                                                 json=json.loads(test_data['data']),
                                                 headers=json.loads(test_data['headers']))
            print(json_data)
            member_id = jsonpath(json_data, '$..id')[0]
            token_type = jsonpath(json_data, '$..token_type')[0]
            token = jsonpath(json_data, '$..token')[0]
            Authorization = " ".join([token_type, token])

        amount_sql = "SELECT * FROM member WHERE id=%s;"
        db_amount_data = self.MH.select_sql(amount_sql, args=(member_id,))
        before_amount = db_amount_data["leave_amount"]

        # 5. 替换member_id
        if ('#member_id#' in test_data["data"]):
            test_data["data"] = test_data["data"].replace("#member_id#", str(member_id))
            # print(test_data)
        if ('*wrong_member_id*' in test_data["data"]):
            while True:
                gen_member_id = helper.generate_member_id()
                # 查询数据库，如果数据库当中存在该member_id，那么我们再生成一次，直到不存在为止
                member_sql = "SELECT * FROM member WHERE id=%s;"
                db_id_data = self.MH.select_sql(member_sql, args=(gen_member_id,))
                if not db_id_data:
                    break
            # 错误的用户名：将member_id 加1或减1赋值给wrong_member_id
            test_data["data"] = test_data["data"].replace('*wrong_member_id*', str(gen_member_id))
            print("我是错误的id:",test_data["data"])
        # 读取excel，得到字典
        headers = json.loads(test_data["headers"])
        # 6. 添加Authorization到headers
        headers["Authorization"] = Authorization
        # 7. 发送请求
        json_data = self.req.request_handler(test_data['method'],
                                             url=(dev_settings.host + test_data['url']),
                                             json=json.loads(test_data['data']),
                                             headers=headers)


        try:
            try:
                # 8. 第一次断言：状态码
                for k,v in json.loads(test_data["expected"]).items():
                    if k in json_data:
                        self.assertEqual(json_data[k],v)
                        self.EH.write_back(
                            file_name=dev_settings.test_data_path,
                            sheet_name=yaml_data['excel']['sheet'][6],
                            row=int(test_data['case_id']) + 1,
                            column=9,
                            write_value='测试通过')
            except AssertionError as e:
                logger.error('用例测试失败：{}'.format(e))
                self.EH.write_back(
                    file_name=dev_settings.test_data_path,
                    sheet_name=yaml_data['excel']['sheet'][6],
                    row=int(test_data['case_id']) + 1,
                    column=9,
                    write_value='测试失败')
                raise e
           # 9. 第二次断言，如果为成功用例进行数据库金额校验，
           # 判断是否是成功用例，如果是则校验数据
            if (json_data["code"] == 0):
                if ("login" not in test_data["url"]):
                    excepted_amount = json.loads(test_data["data"])["amount"]

                    db_amount_data = self.MH.select_sql(amount_sql, args=(member_id,))
                    after_amount = db_amount_data["leave_amount"]
                    # 实际提现金额 = 提现前余额 - 提现后余额
                    # self.assertEqual(before_amount - after_amount, decimal.Decimal(excepted_amount))
                    self.assertEqual(before_amount - decimal.Decimal(excepted_amount), after_amount)
                self.EH.write_back(
                        file_name=dev_settings.test_data_path,
                        sheet_name=yaml_data['excel']['sheet'][6],
                        row=int(test_data['case_id']) + 1,
                        column=9,
                        write_value='测试通过')
        except AssertionError as e:
            logger.error('测试用例失败：{}'.format(e))
            self.EH.write_back(
                file_name=dev_settings.test_data_path,
                sheet_name=yaml_data['excel']['sheet'][6],
                row=int(test_data['case_id']) + 1,
                column=9,
                write_value='测试失败')
            raise e


if __name__ == '__main__':
    TestWithdrawMethod2().test_withdraw_method2()