#coding=utf-8

import rsa
import binascii
import requests
from base64 import b64decode
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class LBTuChongNet(object):
    def __init__(self):
        self.loginUrl = "https://tuchong.com/rest/accounts/login"
        self.userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        self.headers = {
            'user-agent': self.userAgent
        }
        #pubkey 在页面的js中: http://static.tuchong.net/js/pc/page/welcome_6e7f1cd.js
        
        self.key = "D8CC0180AFCC72C9F5981BDB90A27928672F1D6EA8A57AF44EFFA7DAF6EFB17DAD9F643B9F9F7A1F05ACC2FEA8DE19F023200EFEE9224104627F1E680CE8F025AF44824A45EA4DDC321672D2DEAA91DB27418CFDD776848F27A76E747D53966683EFB00F7485F3ECF68365F5C10C69969AE3D665162D2EE3A5BA109D7DF6C7A5"
        self.session = requests.session()
    
    def get_crypt_password(self,message):
        rsaPublickey = int(self.key, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)
        password = rsa.encrypt(message, key)
        password = binascii.b2a_hex(password)
        return password
    
    def get_captcha(self):
        captchaUrl="https://tuchong.com/rest/captcha/image"
        
        rsp = self.session.post(captchaUrl, data = None, headers = self.headers).json()
        captcha_id = rsp['captchaId']
        captcha_base64 = rsp['captchaBase64']
        captcha_base64 = captcha_base64.replace("data:image/png;base64,","")
        with open("lbcaptcha.png",'w') as f:
            f.write(b64decode(captcha_base64))
        captcha = input(u'输入当前目录下 lbcaptcha.png 上的验证码：')
        return captcha_id,captcha
    
    def login(self,username,password):
        
        passwd_crypt = self.get_crypt_password(password)
        postdata = {
            'account': username,
                'password': passwd_crypt,
        }
        rsp = self.session.post(self.loginUrl, data = postdata, headers = self.headers)
        rsp = rsp.json()
        print(rsp)
        #登录成功
        if rsp.has_key('result') and rsp['result'] == "SUCCESS":
            print(rsp['message'])
            return
        
        #登录失败
        if rsp.has_key('code') and rsp.has_key('message'):
            print("response code:%d, message:%s"%(rsp['code'],rsp['message']))
            if rsp['message'].find("验证码") >= 0:
                print(rsp['message'])
                captcha = self.get_captcha()
                postdata = {
                    'account': username,
                    'password': passwd_crypt,
                    'captcha_id': captcha[0],
                    'captcha_token': int(captcha[1])
                }
                rsp = self.session.post(self.loginUrl, data = postdata, headers = self.headers)
                if str(rsp).find('200'):
                    print("登陆成功！")


if __name__ == '__main__':
    # 图虫网验证
    lbtuchongnet = LBTuChongNet()
    username = raw_input(u'请输入图虫网用户名：')
    password = raw_input(u'请输入图虫网密码：')
    lbtuchongnet.login(username,password)
