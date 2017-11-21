# -*- coding:utf-8 -*-

from selenium import webdriver
import time
driver = webdriver.PhantomJS(executable_path="./phantomjs-2.1.1-macosx/bin/phantomjs")
driver.get("https://www.baidu.com/")

# 给搜索输入框标红的javascript脚本
js = "var q=document.getElementById(\"kw\");q.style.border=\"2px solid red\";"

# 调用给搜索输入框标红js脚本
driver.execute_script(js)

# 查看页面快照
driver.save_screenshot("redbaidu.png")

# js隐藏元素，将获取的图片元素隐藏
img = driver.find_element_by_xpath("//div[@id='lg']/img")
driver.execute_script('$(arguments[0]).fadeOut()',img)

# 向下滚动到页面底部
# driver.execute_script("$('.scroll_top').click(function(){$('html,body').animate({scrollTop: '0px'}, 800);});")
time.sleep(1)
# 查看页面快照
driver.save_screenshot("wubaidu.png")

driver.quit()