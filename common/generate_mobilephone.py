# -- encoding: utf-8 --
# @time:    2020/12/5 20:47
# @Author: jsonLiu
# @Email: 810030709@qq.com
# @file: generate_mobilephone.py
import random
import string


class GenerateMobilePhone:
    def generate_mobile_phone(self):
        # start = '1' + random.choice(['3','5','7','8','9'])
        # end = ''.join(random.sample(string.digits, 9))
        # phone_number = start + end
        # return phone_number
        phone = '1' + random.choice(['3','5','7','8','9'])
        for i  in range(9):
            end = random.randint(1,9)
            phone += str(end)
        return phone
if __name__ == '__main__':
    mobile_phone = GenerateMobilePhone().generate_mobile_phone()
    print(mobile_phone)