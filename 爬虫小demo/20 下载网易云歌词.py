#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib import request

# 1、获取网页
def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36 OPR/49.0.2725.47',
        'Referer': 'http://music.163.com/',
        'Host': 'music.163.com'
        }

    try:
        response = requests.get(url, headers=headers)
        html = response.text
        return html
    except:
        print('request error')

def get_text(song_id):
    url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(song_id) + '&lv=1&kv=1&tv=-1'
    html = get_html(url)
    json_obj = json.loads(html)
    text = json_obj['lrc']['lyric']
    regex = re.compile(r'\[.*\]')
    finalLyric = re.sub(regex, '', text).strip()
    return finalLyric

def write_text(song_name,text):
    print("正在写入歌曲：{}".format(song_name))
    with open("{}.txt".format(song_name),'a',encoding='utf-8') as fp:
        fp.write(text)

def getSingerInfo(html):
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find('ul', class_='f-hide').find_all('a')
    song_IDs = []
    song_names = []
    for link in links:
        song_ID = link.get('href').split('=')[-1]
        song_name = link.get_text()
        song_IDs.append(song_ID)
        song_names.append(song_name)
    return zip(song_names, song_IDs)

def downloadSong(songName,songId):
    singer_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(songId)
    print('正在下载歌曲:{}'.format(songName))
    request.urlretrieve(singer_url,'{}.mp3'.format(songName))



if __name__ == "__main__":
    singerId = input("请输入歌手的ID：")
    startUrl = "http://music.163.com/artist?id={}".format(singerId)
    html = get_html(startUrl)
    singerInfos = getSingerInfo(html)

    for singerInfo in singerInfos:
        print(singerInfo[1],singerInfo[0])
        text = get_text(singerInfo[1])
        # 下载歌曲文本
        write_text(singerInfo[0],text)
        # 下载歌曲mp3
        downloadSong(singerInfo[0],singerInfo[1])




