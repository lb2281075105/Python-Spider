import time
from selenium import webdriver
from lxml import etree

driver = webdriver.PhantomJS(executable_path='./phantomjs-2.1.1-macosx/bin/phantomjs')


# 获取第一页的数据
def get_html():
    url = "https://detail.tmall.com/item.htm?id=531993957001&skuId=3609796167425&user_id=268451883&cat_id=2&is_b=1&rn=71b9b0aeb233411c4f59fe8c610bc34b"
    driver.get(url)
    time.sleep(5)
    driver.execute_script('window.scrollBy(0,3000)')
    time.sleep(2)
    driver.execute_script('window.scrollBy(0,5000)')
    time.sleep(2)

    # 累计评价
    btnNext = driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[3]/a')
    btnNext.click()
    html = driver.page_source
    return html


def get_comments(html):
    source = etree.HTML(html)
    commens = source.xpath("//*[@id='J_TabBar']/li[3]/a/em/text()")
    print('评论数：', commens)
    # 将评论转为int类型
    commens = (int(commens[0]) / 20) + 1
    # 获取到总评论
    print('评论数：', int(commens))
    return int(commens)


def parse_html(html):
    html = etree.HTML(html)
    commentlist = html.xpath("//*[@class='rate-grid']/table/tbody")
    for comment in commentlist:
        # 评论
        vercomment = comment.xpath(
            "./tr/td[@class='tm-col-master']/div[@class='tm-rate-content']/div[@class='tm-rate-fulltxt']/text()")
        # 机器类型
        verphone = comment.xpath("./tr/td[@class='col-meta']/div[@class='rate-sku']/p[@title]/text()")
        print(vercomment)
        print(verphone)
        # 用户(头尾各一个字，中间用****代替)
        veruser = comment.xpath("./tr/td[@class='col-author']/div[@class='rate-user-info']/text()")
        print(veruser)


def next_button_work(num):
    if num != 0:
        driver.execute_script('window.scrollBy(0,3000)')
        time.sleep(2)
        try:
            driver.find_element_by_css_selector('#J_Reviews > div > div.rate-page > div > a:last-child').click()
        except Exception as e:
            print(e)

        time.sleep(2)
        driver.execute_script('window.scrollBy(0,3000)')
        time.sleep(2)
        driver.execute_script('window.scrollBy(0,5000)')
        time.sleep(2)
        html = driver.page_source
        parse_html(html)


def selenuim_work(html):
    parse_html(html)
    next_button_work(1)
    pass


def gettotalpagecomments(comments):
    html = get_html()
    for i in range(0, comments):
        selenuim_work(html)


data = get_html()
# 得到评论
commens = get_comments(data)
# 根据评论内容进行遍历
gettotalpagecomments(commens)
