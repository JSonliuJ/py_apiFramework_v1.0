# -- encoding: utf-8 --
# @time:    	2020/12/27 21:48
# @Author: 		jsonLiu
# @Email:  		810030709@qq.com
# @file: 		test_010_info_method2
import json
import os
import unittest
from jsonpath import jsonpath
from common.excelhandler import ExcelHandle
from common.requesthandler import RequestHandler
from config.settings import dev_settings
from lib import ddt
from middleware import helper
from middleware.db_handler import DBHandler
from middleware.get_yaml_data import yaml_data
from middleware.log_handler import logger


@ddt.ddt
class TestInfoMethod2(unittest.TestCase):
    EH = ExcelHandle(dev_settings.test_data_path)
    data = EH.read_all_data(yaml_data['excel']['sheet'][16])
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
    def test_010_info_method2(self, test_data):
        global member_id, Authorization, wrong_member_id, json_data
        if "login" in test_data["url"]:
            json_data = self.req.request_handler(test_data['method'],
                                                 url=(dev_settings.host + test_data['url']),
                                                 json=json.loads(test_data['data']),
                                                 headers=json.loads(test_data['headers']))
            member_id = jsonpath(json_data, '$..id')[0]
            token_type = jsonpath(json_data, '$..token_type')[0]
            token = jsonpath(json_data, '$..token')[0]
            Authorization = " ".join([token_type, token])
            print(json_data)
        # 5. 替换member_id
        if '#member_id#' in test_data["url"]:
            test_data["url"] = test_data["url"].replace("#member_id#", str(member_id))
        if '*wrong_member_id*' in test_data["url"]:
            while True:
                member_sql1 = "SELECT * FROM member where type='1' limit 1;"
                db_id_data1 = self.MH.select_sql(member_sql1)
                wrong_member_id = int(db_id_data1["id"])
                if int(wrong_member_id) != int(member_id):
                    break
            test_data["url"] = test_data["url"].replace("*wrong_member_id*",str(wrong_member_id))
        if '*no_exist_member_id*' in test_data["url"]:
            while True:
                gen_member_id = helper.generate_member_id()
                # 查询数据库，如果数据库当中存在该member_id，那么我们再生成一次，直到不存在为止
                member_sql2 = "SELECT * FROM member WHERE id=%s;"
                db_id_data2 = self.MH.select_sql(member_sql2, args=(gen_member_id,))
                if not db_id_data2:
                    break
            # 不存在的用户名：
            test_data["url"] = test_data["url"].replace('*no_exist_member_id*', str(gen_member_id))
        print(test_data)
        # 读取excel，得到字典
        headers = json.loads(test_data["headers"])
        # 6. 添加Authorization到headers
        headers["Authorization"] = Authorization
        # 7. 发送请求
        if test_data["module_name"] == "info":
            json_data = self.req.request_handler(test_data['method'],
                                             url=(dev_settings.host + test_data['url']),
                                             headers=headers)
        print(json_data)
        try:
            try:
                # 8. 第一次断言：状态码
                for k, v in json.loads(test_data["expected"]).items():
                    if k in json_data:
                        self.assertEqual(json_data[k], v)
                        self.EH.write_back(
                            file_name=dev_settings.test_data_path,
                            sheet_name=yaml_data['excel']['sheet'][16],
                            row=int(test_data['case_id']) + 1,
                            column=9,
                            write_value='测试通过')
            except AssertionError as e:
                logger.error('用例测试失败：{}'.format(e))
                self.EH.write_back(
                    file_name=dev_settings.test_data_path,
                    sheet_name=yaml_data['excel']['sheet'][16],
                    row=int(test_data['case_id']) + 1,
                    column=9,
                    write_value='测试失败')
                raise e
            # 9. 第二次断言，如果为成功用例进行数据库member_id检验，
            # 判断是否是成功用例，如果是则校验数据
            if not json_data["code"]:
                if "login" not in test_data["url"]:
                    sql = test_data['sql_check']
                    member_info = self.MH.select_sql(sql, args=(member_id,))
                    logger.info("用户信息：".format(member_info))
                    self.assertTrue(member_info)
                    self.EH.write_back(
                        file_name=dev_settings.test_data_path,
                        sheet_name=yaml_data['excel']['sheet'][16],
                        row=int(test_data['case_id']) + 1,
                        column=9,
                        write_value='测试通过')
        except AssertionError as e:
            logger.error('测试用例失败：{}'.format(e))
            self.EH.write_back(
                file_name=dev_settings.test_data_path,
                sheet_name=yaml_data['excel']['sheet'][16],
                row=int(test_data['case_id']) + 1,
                column=9,
                write_value='测试失败')
            raise e


if __name__ == '__main__':
    unittest.main()
