# -*- coding:utf-8 -*-
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

driver = webdriver.PhantomJS(executable_path="./phantomjs-2.1.1-macosx/bin/phantomjs")
driver.get("http://baidu.com/")

driver.find_element_by_id("kw").send_keys(u"长城")
sleep(10)
driver.find_element_by_id("su").click()

driver.save_screenshot("长城.png")

