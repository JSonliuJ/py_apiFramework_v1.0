# -- encoding: utf-8 --
# @time:    2020/12/5 14:32
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: myslqhandler.py
import pymysql
# 初始化连接
from pymysql.cursors import DictCursor


class MysqlHandler:
    def __init__(self,host,port,
                 user,password,
                 database,charset='utf8',
                 cursorclass=DictCursor,
                 **kwargs):
        # 建立连接
        self.conn = pymysql.connect(host=host,port=port,
                                    user=user,password=password,
                                    database=database,charset=charset,
                                    cursorclass=cursorclass,
                                    **kwargs)

        # 初始化游标
        self.cursor = self.conn.cursor()
    def insert_sql(self,sql):
        """
        # 一行插入格式：
        insert into 表名 values()
        insert into 表名(字段1,字段2,...) values(值1,值2,...)
        # 多行插入方式1：
        insert into 表名 values
        (),
        (),
        ()
        # 多行插入方式2：
        insert into 表名(列1,列2,列3,列4) values
        (值1,值2,....,值n),
        (值1,值2,....,值n),
        (值1,值2,....,值n)
        """
        self.cursor.execute(sql)
        self.conn.commit()
    def update_sql(self,sql):
        # 修改：update 表名 set 列1=值1,列2=值2,....where 条件;
        self.cursor.execute(sql)
        self.conn.commit()
    def delete_sql(self,sql):
        # 删除：delete form 表名 where 条件;
        self.cursor.execute(sql)
        self.conn.commit()
    def select_sql(self,sql,args=None,one=True):
        # 查询 select 字段名 from 表名 where 条件;
        self.cursor.execute(sql,args)
        # TODO: 提交事务(数据同步)
        self.conn.commit()
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    from config.settings import dev_settings
    from common.yamlhandler import YamlHandler
    config_data = YamlHandler().read_yaml(file=dev_settings.conf_yaml_path)
    print(config_data['database'])
    MH = MysqlHandler(host=config_data['database']['host'],
                      port=config_data['database']['port'],
                      user=config_data['database']['user'],
                      password=config_data['database']['password'],
                      database=config_data['database']['database'],
                      charset=config_data['database']['charset'])
    sql = "select * from member limit 1;"
    select_data = MH.select_sql(sql)
    # MH.close()
    print(type(select_data['mobile_phone']))
