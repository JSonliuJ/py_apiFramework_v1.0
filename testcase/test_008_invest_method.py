# -- encoding: utf-8 --
# @time:    	2020/12/24 0:17
# @Author: 		jsonLiu
# @Email:  		810030709@qq.com
# @file: 		test_008_invest_method
import json
import os
import unittest
from common.excelhandler import ExcelHandle
from common.requesthandler import RequestHandler
from config.settings import dev_settings
from lib import ddt
from middleware import helper
from middleware.db_handler import DBHandler
from middleware.get_yaml_data import yaml_data
from middleware.invest_helper import Context


@ddt.ddt
class TestRechargeMethod(unittest.TestCase):
    EH = ExcelHandle(dev_settings.test_data_path)
    data = EH.read_all_data(yaml_data['excel']['sheet'][11])
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
    def test_recharge_method1(self, test_data):
        Authorization = Context().token
        member_id = Context().member_id
        loan_id = Context().loan_id
        amount_sql = "SELECT * FROM member WHERE id=%s;"
        db_amount_data = self.MH.select_sql(amount_sql, args=(member_id,))
        before_amount = db_amount_data["leave_amount"]

        # 5. 替换member_id和loan_id
        if '#member_id#' in test_data["data"]:
            test_data["data"] = test_data["data"].replace("#member_id#", str(member_id))
        if "#loan_id#" in test_data["data"]:
            test_data["data"] = test_data["data"].replace("#loan_id#", str(loan_id))
        if '*no_exist_member_id*' in test_data["data"]:
            while True:
                gen_member_id = helper.generate_member_id()
                # 查询数据库，如果数据库当中存在该member_id，那么我们再生成一次，直到不存在为止
                member_sql2 = "SELECT * FROM member WHERE id=%s;"
                db_id_data2 = self.MH.select_sql(member_sql2, args=(gen_member_id,))
                if not db_id_data2:
                    break
            # 不存在的用户名：
            test_data["data"] = test_data["data"].replace('*no_exist_member_id*', str(gen_member_id))
        if '*wrong_member_id*' in test_data["data"]:
            while True:
                member_sql1 = "SELECT * FROM member where type='1' limit 1;"
                db_id_data1 = self.MH.select_sql(member_sql1)
                wrong_member_id = db_id_data1["id"]
                if wrong_member_id != member_id:
                    break
            test_data["data"] = test_data["data"].replace("*wrong_member_id*", str(wrong_member_id))
        if '*no_exist_loan_id*' in test_data["data"]:
            while True:
                gen_add_loan_id = helper.generate_add_loan_id()
                # 查询数据库，如果数据库当中存在该member_id，那么我们再生成一次，直到不存在为止
                sql = "SELECT id FROM loan WHERE id=%s;"
                db_id_data = self.MH.select_sql(sql, args=(gen_add_loan_id,))
                if not db_id_data:
                    break
            # 错误的借款id：将loan_id 加1或减1赋值给loan_id
            test_data["data"] = test_data["data"].replace('*no_exist_loan_id*', str(gen_add_loan_id))
        # 非竞标中的项目id
        if "*no_invest_loan*" in test_data["data"]:
            sql = "select * from loan where status <> 2 limit 1;"
            no_invest_loan_id_data = self.MH.select_sql(sql)
            if no_invest_loan_id_data:
                test_data["data"] = test_data["data"].replace('*no_invest_loan*', str(no_invest_loan_id_data["id"]))
        # # 读取excel，得到字典
        print(test_data)
        headers = json.loads(test_data["headers"])
        # # 6. 添加Authorization到headers
        headers["Authorization"] = Authorization
        # # 7. 发送请求
        json_data = self.req.request_handler(test_data['method'],
                                             url=(dev_settings.host + test_data['url']),
                                             json=json.loads(test_data['data']),
                                             headers=headers)
        print(json_data)
        # try:
        #     try:
        #         # 8. 第一次断言：状态码
        #         for k, v in json.loads(test_data["expected"]).items():
        #             if k in json_data:
        #                 self.assertEqual(json_data[k], v)
        #                 self.EH.write_back(
        #                     file_name=dev_settings.test_data_path,
        #                     sheet_name=yaml_data['excel']['sheet'][11],
        #                     row=int(test_data['case_id']) + 1,
        #                     column=9,
        #                     write_value='测试通过')
        #     except AssertionError as e:
        #         logger.error('用例测试失败：{}'.format(e))
        #         self.EH.write_back(
        #             file_name=dev_settings.test_data_path,
        #             sheet_name=yaml_data['excel']['sheet'][11],
        #             row=int(test_data['case_id']) + 1,
        #             column=9,
        #             write_value='测试失败')
        #         raise e
        #     # 9. 第二次断言，如果为成功用例进行数据库金额校验，
        #     # 判断是否是成功用例，如果是则校验数据
        #     if not json_data["code"]:
        #         excepted_amount = json.loads(test_data["data"])["amount"]
        #
        #         db_amount_data = self.MH.select_sql(amount_sql, args=(member_id,))
        #         after_amount = db_amount_data["leave_amount"]
        #         # 实际充值金额 = 充值后金额 - 充值前金额
        #         self.assertEqual(before_amount + decimal.Decimal(excepted_amount), after_amount)
        #
        #         self.EH.write_back(
        #             file_name=dev_settings.test_data_path,
        #             sheet_name=yaml_data['excel']['sheet'][11],
        #             row=int(test_data['case_id']) + 1,
        #             column=9,
        #             write_value='测试通过')
        # except AssertionError as e:
        #     logger.error('测试用例失败：{}'.format(e))
        #     self.EH.write_back(
        #         file_name=dev_settings.test_data_path,
        #         sheet_name=yaml_data['excel']['sheet'][11],
        #         row=int(test_data['case_id']) + 1,
        #         column=9,
        #         write_value='测试失败')
        #     raise e


if __name__ == '__main__':
    unittest.main()
