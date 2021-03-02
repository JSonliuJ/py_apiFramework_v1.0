# -- encoding: utf-8 --
# @time:    	2020/12/26 0:32
# @Author: 		jsonLiu
# @Email:  		810030709@qq.com
# @file: 		invest_helper
from jsonpath import jsonpath

from middleware.db_handler import DBHandler
from middleware.helper import login, admin_login


class Context:
    @property
    def loan_id(self):
        """查询数据库，得到loan_id，
        临时变量保存到Context当中
        retrun 返回loan当中的id值
        """
        sql = "SELECT * from loan WHERE status=2 limit 1;"
        db = DBHandler()
        loanId = db.select_sql(sql=sql)["id"]
        db.close()
        return loanId

    @property
    def token(self):
        json_data = login()
        token_type = jsonpath(json_data, '$..token_type')[0]
        t = jsonpath(json_data, '$..token')[0]
        Authorization = " ".join([token_type, t])
        return Authorization

    @property
    def admin_token(self):
        json_data = admin_login()
        token_type = jsonpath(json_data, '$..token_type')[0]
        t = jsonpath(json_data, '$..token')[0]  # 不能命名为token，否则与函数名同名
        admin_Authorization = " ".join([token_type, t])
        return admin_Authorization

    @property
    def member_id(self):
        json_data = login()
        mem_id = jsonpath(json_data, '$..id')[0]
        return mem_id


if __name__ == '__main__':
    # print(Context().token)

    # print(Context().admin_token)

    print(Context().loan_id)

    # print(Context().member_id)
