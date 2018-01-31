# -*- coding:utf-8 -*-


# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
#
# driver = webdriver.PhantomJS(executable_path="/Users/yunmei/phantomjs-2.1.1-macosx/bin/phantomjs")
# driver.get("https://www.douban.com/")
#
# # 输入账号密码
# driver.find_element_by_name("form_email").send_keys("2334497007@qq.com")
# driver.find_element_by_name("form_password").send_keys("lbaiwb1314")
#
# # 模拟点击登录
# driver.find_element_by_xpath("//input[@class='bn-submit']").click()
#
# # 等待3秒
# time.sleep(3)
#
# # 生成登陆后快照
# driver.save_screenshot("douban.png")
#
# with open("douban.html", "w") as file:
#     file.write(driver.page_source.encode('utf-8'))
#
# driver.quit()


from selenium import webdriver
import time
# 创建浏览器对象
browser=webdriver.PhantomJS(executable_path="/Users/yunmei/phantomjs-2.1.1-macosx/bin/phantomjs")
# 请求加载登录链接
browser.get('https://www.zhihu.com/#signin')
time.sleep(3)
# 模拟点击使用密码登录
browser.find_element_by_css_selector(".signin-switch-password").click()
# 输入账号
browser.find_element_by_css_selector(".account input[name='account']").send_keys('17078075655')
# 输入密码
browser.find_element_by_css_selector(".verification input[name='password']").send_keys('19910825580lb')
# 模拟点击登录
browser.find_element_by_css_selector(".sign-button").click()
time.sleep(3)
# 截图
browser.save_screenshot("zhihu.png")
browser.quit()