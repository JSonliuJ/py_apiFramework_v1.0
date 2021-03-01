# -- encoding: utf-8 --
# @time:    2020/12/5 13:36
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: requesthandler.py
import requests

class RequestHandler(object):
    """
    请求一个接口，可以使用get、post、delete、put
    请求地址：url
    请求参数：params、data、json
    """
    def __init__(self):
        self.session = requests.Session()

    def request_handler(self, method, url, params=None, data=None, json=None, **kwargs):
        # if method.uper() == 'GET':
        #     res = self.session.get(url,params=params,**kwargs)
        # elif method.uper() == 'POST':
        #     res = self.session.post(url,params=params,data=data,json=json,**kwargs)
        # else:
        #    res =  self.session.request(method,url,params=params,data=data,json=json,**kwargs)
        # try:
        #     return res.json()
        # except ValueError:
        #     print('not json')

        res = self.session.request(method, url, params=params, data=data, json=json, **kwargs)
        try:
            return res.json()
        except ValueError:
            print('not json')

    def close_session(self):
        self.session.close()
if __name__ == '__main__':
    method = 'POST'
    url = 'http://120.78.128.25:8766/futureloan/member/register'
    headers = {
        'X-Lemonban-Media-Type': 'lemonban.v2',
        'Connection':'close',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4315.5 Safari/537.36'
    }
    data = {
        # "mobile_phone": "13743211235",
        "mobile_phone":"13743218881",
        "pwd": "123456abc"
    }
    res = RequestHandler().request_handler(method, url, headers=headers, json=data)
    print(res.text)
    # print(res.content)