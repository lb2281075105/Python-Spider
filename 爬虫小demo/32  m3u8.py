import requests
import re
from Crypto.Cipher import AES

def m3u8(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # requests得到m3u8文件内容
    content = requests.get(url, headers=header).text
    if "#EXTM3U" not in content:
        print("这不是一个m3u8的视频链接！")
        return False
    if "EXT-X-KEY" not in content:
        print("没有加密")
        return False

    # 使用re正则得到key和视频地址
    jiami = re.findall('#EXT-X-KEY:(.*)',content)
    key = re.findall('URI="(.*)"', jiami[0])
    vi = re.findall('IV=(.*)', jiami[0])[0]

    # 得到每一个ts视频链接

    # tslist = re.findall('EXTINF:(.*), (. *)',content.replace(' ', '').replace(r'\n', ''))
    tslist = re.findall('v.f240.ts(.*)',content)

    newlist = []
    for i in tslist:
        newlist.append("v.f240.ts" + i)
    # print(newlist)
    # 得到key的链接并请求得到加密的key值
    keyurl = key[0]
    keycontent = requests.get(keyurl, headers=header).content

    # 得到每一个完整视频的链接地址
    base_url = url.replace(url.split('/')[-1], '')
    # print(base_url)
    tslisturl = []
    for i in newlist:
        tsurl = base_url + i
        tslisturl.append(tsurl)

    # 得到解密方法，这里要导入第三方库  pycrypto
    # 这里有一个问题，安装pycrypto成功后，导入from Crypto.Cipher import AES报错
    # 找到使用python环境的文件夹，在Lib文件夹下有一个 site-packages 文件夹，里面是我们环境安装的包。
    # 找到一个crypto文件夹，打开可以看到 Cipher文件夹，此时我们将 crypto文件夹改为 Crypto 即可使用了
    # 必须添加b'0000000000000000'，防止报错ValueError: IV must be 16 bytes long
    cryptor = AES.new(keycontent, AES.MODE_CBC, b'0000000000000000')

    # for循环获取视频文件
    for i in tslisturl:
        print(i)
        res = requests.get(i, header)
        # 使用解密方法解密得到的视频文件
        cont = cryptor.decrypt(res.content)
    # 以追加的形式保存为mp4文件，mp4可以随意命名，这里命名为小鹅通视频下载测试
        with open('14-搜索组件界面实现.mp4', 'ab+') as f:
            f.write(cont)
    return True

if __name__ == '__main__':
    # 这个是网页上查到的小鹅通的卖u8地址
    # url = "https://1252524126.vod2.myqcloud.com/9764a7a5vodtransgzp1252524126/91c29aad5285890807164109582/drm/v.f146750.m3u8"
    # url = "https://1258102968.vod2.myqcloud.com/ed7d8254vodtranscq1258102968/a61912e43701925923160746329/drm/v.f240.m3u8?t=62dfad73&us=DYws6oOg3A&sign=1d4381d06b276e87eae478a23f3d6375"
    url = "https://1258102968.vod2.myqcloud.com/ed7d8254vodtranscq1258102968/a3ae8ff93701925923160630524/drm/v.f240.m3u8?t=62dfaf5a&us=RquNSsL6XT&sign=8bec9ca974f9413c9bad7a9e8d620ae2"
    pd = m3u8(url)
    if pd:
      print('视频下载完成！')