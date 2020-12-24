import requests
from lxml import html
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def star(url):
    url2 = "https://api.bilibili.com/x/player/playurl?avid={avid}&cid={cid}&qn=32&type=&otype=json"
    headers2 = {
        "host": "",
        "Referer": "https://www.bilibili.com",
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;WOW64) AppleWebKit/537.36(KHTML,likeGecko)Chrome/63.0.3239.132Safari/537.36"
    }

    avid = re.findall("video/av(.+)\?", url)
    print(avid)
    cid ,name = get_cid(avid[0])
    print(cid,name)
    flv_url , size = get_flvurl(url2.format(avid=avid[0],cid=cid))
    shuju = size / 1024 / 1024
    print("本视频大小为：%.2fM" % shuju)

    h = re.findall("https://(.+)com",flv_url)
    host = h[0]+"com"

    headers2["host"] = host
    res = requests.get(flv_url,headers=headers2,stream=True, verify=False)
    print(res.status_code)
    save_movie(res,name)

def get_cid(aid):#获得cid
    header = {
        'host': 'api.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
             }
    url = "https://api.bilibili.com/x/player/pagelist?aid={aid}&jsonp=jsonp".format(aid=aid)
    response = requests.get(url,headers=header).json()
    # print(response["data"])
    # 这个地方设置index是因为下载集合里面的视频,顺序,0代表下载第一个视频,1代表下载集合里面第二个视频,2,3,4...依次类推
    index = 0
    return response["data"][index]["cid"] ,response["data"][index]["part"]
def get_flvurl(url):#获得视频真实flv地址
    header = {'host': 'api.bilibili.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

    response = requests.get(url,headers=header).json()
    return response["data"]["durl"][0]["url"],response["data"]["durl"][0]["size"]
def save_movie(res,name):#保存视频
    chunk_size = 1024
    with open("{name}.flv".format(name = name),"wb") as f:
        for data in res.iter_content(1024):
            f.write(data)


if __name__ == "__main__":
    # 把下面的av后面的'583959574'在要下载的视频集合里面找到就可以下载视频了
    url = "https://www.bilibili.com/video/av583959574?spm_id_from=333.334.b_62696c695f646f756761.5"
    star(url)


