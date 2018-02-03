# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time

class JDlogin():
    def __init__(self, username, password):
        self.session = requests.session()
        self.loginUrl = "http://passport.jd.com/uc/login"
        self.postUrl = "http://passport.jd.com/uc/loginService"
        self.authUrl = "https://passport.jd.com/uc/showAuthCode"
        self.username = username
        self.password = password

        # 设置请求头
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            }

    def get_authcode(self, url):
        self.headers['Host'] = 'authcode.jd.com'
        self.headers['Referer'] = 'https://passport.jd.com/uc/login'
        response = self.session.get(url, headers=self.headers)
        with open('codeimage.jpg', 'wb') as f:
            f.write(response.content)
        authcode = input("请输入验证码：")
        return authcode

    def get_info(self):

        try:
            # 登陆请求
            html = self.session.get(self.loginUrl, headers=self.headers)
            soup = BeautifulSoup(html.text,"lxml")
            inputList = soup.select('.form input')
            print(inputList)
            data = {}
            data['uuid'] = inputList[0]['value']
            data['eid'] = inputList[4]['value']
            data['fp'] = inputList[5]['value']
            data['_t'] = inputList[6]['value']
            rstr = inputList[7]['name']
            data[rstr] = inputList[7]['value']
            acRequired = self.session.post(self.authUrl, data={
                'loginName': self.username}).text

            if 'true' in acRequired:

                acUrl = soup.select('.form img')[0]['src2']
                acUrl = 'http:{}&yys={}'.format(acUrl, str(int(time.time() * 1000)))
                authcode = self.get_authcode(acUrl)
                data['authcode'] = authcode
            else:
                data['authcode'] = ''

        except Exception as e:
            print(e)
        finally:
            return data

    def jd_login(self):

        data = self.get_info()
        # Form表单提交数据
        # 1、loginname、nloginpwd、loginpwd是在网页中input属性值name,作为表单值提交到登陆请求
        # 2、在此处也可以用selenium来进行给输入框(登陆账号、登陆密码)进行赋值

        data['loginname'] = self.username
        data['nloginpwd'] = self.password
        data['loginpwd'] = self.password
        try:
            self.headers['Host'] = 'passport.jd.com'
            html = self.session.post(self.postUrl, data=data, headers=self.headers)
            # 在这里可以判断请求是否判断成功不成功
            print(html.text)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # 在下面输入账号名、密码
    jdlogin = JDlogin("******", "******")
    jdlogin.jd_login()
