# -- encoding: utf-8 --
# @time:    2020/12/6 23:07
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: test_003_recharge_method1.py
# self.req.visit() 访问登录接口，res得到token
import decimal
import json
import os
import unittest
from lib import ddt
from common.excelhandler import ExcelHandle
from common.requesthandler import RequestHandler
from config.settings import dev_settings
from middleware.get_yaml_data import yaml_data
from middleware import helper
from middleware.helper import Context, save_token
from middleware.log_handler import logger
from middleware.db_handler import DBHandler
@ddt.ddt
class TestRechargeMethod(unittest.TestCase):
    EH = ExcelHandle(dev_settings.test_data_path)
    data = EH.read_all_data(yaml_data['excel']['sheet'][3])
    log_file = os.path.join(dev_settings.log_path, yaml_data['logger']['file'])

    def setUp(self):
        # 1. 数据库连接
        self.MH = DBHandler()
        # 2. 请求
        self.req = RequestHandler()
        save_token()
    def tearDown(self):
        # 3. 数据库关闭
        self.MH.close()
        # 4. 会话关闭
        self.req.close_session()

    @ddt.data(*data)
    def test_recharge_method1(self, test_data):
        Authorization = Context.Authorization
        member_id = Context.member_id

        amount_sql = "SELECT * FROM member WHERE id=%s;"
        db_amount_data = self.MH.select_sql(amount_sql, args=(member_id,))
        before_amount = db_amount_data["leave_amount"]

        # 5. 替换member_id
        if '#member_id#' in test_data["data"]:
            test_data["data"] = test_data["data"].replace("#member_id#", str(member_id))
            # print(test_data)
        if '*wrong_member_id*' in test_data["data"]:
            while True:
                member_id = helper.generate_member_id()
                # 查询数据库，如果数据库当中存在该member_id，那么我们再生成一次，直到不存在为止
                member_sql = "SELECT * FROM member WHERE id=%s;"
                db_id_data = self.MH.select_sql(member_sql, args=(member_id,))
                if not db_id_data:
                    break
            # 错误的用户名：将member_id 加1或减1赋值给wrong_member_id
            test_data["data"] = test_data["data"].replace('*wrong_member_id*', str(member_id))
            # print("我是错误的id:",test_data["data"])
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
                # self.assertEqual(json_data["code"], expected)
                for k,v in json.loads(test_data["expected"]).items():
                    if k in json_data:
                        self.assertEqual(json_data[k],v)
                        self.EH.write_back(
                            file_name=dev_settings.test_data_path,
                            sheet_name=yaml_data['excel']['sheet'][3],
                            row=int(test_data['case_id']) + 1,
                            column=9,
                            write_value='测试通过')
            except AssertionError as e:
                logger.error('用例测试失败：{}'.format(e))
                self.EH.write_back(
                    file_name=dev_settings.test_data_path,
                    sheet_name=yaml_data['excel']['sheet'][3],
                    row=int(test_data['case_id']) + 1,
                    column=9,
                    write_value='测试失败')
                raise e
           # 9. 第二次断言，如果为成功用例进行数据库金额校验，
           # 判断是否是成功用例，如果是则校验数据
            if not json_data["code"]:
                excepted_amount = json.loads(test_data["data"])["amount"]

                db_amount_data = self.MH.select_sql(amount_sql, args=(member_id,))
                after_amount = db_amount_data["leave_amount"]
                # 实际充值金额 = 充值后金额 - 充值前金额
                self.assertEqual(before_amount + decimal.Decimal(excepted_amount), after_amount)

                self.EH.write_back(
                    file_name=dev_settings.test_data_path,
                    sheet_name=yaml_data['excel']['sheet'][3],
                    row=int(test_data['case_id']) + 1,
                    column=9,
                    write_value='测试通过')
        except AssertionError as e:
            logger.error('测试用例失败：{}'.format(e))
            self.EH.write_back(
                file_name=dev_settings.test_data_path,
                sheet_name=yaml_data['excel']['sheet'][3],
                row=int(test_data['case_id']) + 1,
                column=9,
                write_value='测试失败')
            raise e


if __name__ == '__main__':
    unittest.main()
