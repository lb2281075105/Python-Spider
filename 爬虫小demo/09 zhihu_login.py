# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time


class Login():
    # 模拟登录一般步骤：(1)首先抓包，根据webForm来分析需要传那些data
    #                (2)分析_xsrf获取
    #                (3)分析验证码获取方式
    #                (4)post登录

    def get_login(self):
        sess=requests.Session()
        # 头部headers需要注意，如果头部没有设置好，下面的步骤就会不能执行成功
        headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0)'}
        # 首先获取登录页面，找到需要get的数据，同时记录cookie的值
        html=sess.get('https://www.zhihu.com/#signin',headers=headers).text
        # 调用xml解析库
        bs=BeautifulSoup(html,'lxml')
        # _xsrf作用是跨站请求伪造(或者叫跨域攻击)
        _xsrf=bs.find('input',attrs={'name':'_xsrf'}).get('value')
        # 通过时间戳拼接验证码链接
        captcha_url='https://www.zhihu.com/captcha.gif?r=%d&type=login'%(time.time()*1000)
        # 发送验证码请求，获取图片数据流。
        captchadata = sess.get(captcha_url, headers=headers).content
        text = self.captcha(captchadata)

        data={
            '_xsrf':_xsrf,
            'phone_num':'17078075655',# 换成邮箱登录也可
            'password':'lbaiwb1314',
            'captcha':text
        }
        response=sess.post('https://www.zhihu.com/login/phone_num',data=data,headers=headers)
        # print type(response.text)
        # 在个人中心请求一下是否真正登录成功
        response=sess.get('https://www.zhihu.com/people/liu-tao-98-32/activities',headers=headers)
        with open("mylogin.txt", "w") as file:
            file.write(response.text.encode("utf-8"))

    def captcha(self,captcha_data):
        # 将二进制数据写入到文件中
        with open('captcha.jpg','wb')as f:
            f.write(captcha_data)
        text=raw_input('请输入登录验证码')
        return text

if __name__=='__main__':

   login = Login()
   login.get_login()
