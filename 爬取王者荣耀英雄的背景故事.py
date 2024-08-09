# -*- coding: UTF-8 -*-
# @Time: 2021/7/18 18:08
# @Author: 远方的星
# @CSDN: https://blog.csdn.net/qq_44921056

import os
import re
import bs4
import requests
import chardet
import logging

# 日志输出的基本配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# 创建一个文件夹
path = './王者故事'
if not os.path.exists(path):
    os.mkdir(path)

headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
              '537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
}


#  获取英雄名称及对应编号
def get_hero_num(url, hero_dream):
    response = requests.get(url=url, headers=headers).text
    # print(response)
    hero_list = re.findall('"ename": (.+?),', response, re.S)  # 得到英雄的编号列表
    hero_name = re.findall('"cname": "(.+?)"', response, re.S)  # 得到英雄的名字列表
    hero_num = hero_name.index(hero_dream)
    num = hero_list[hero_num]  # 得到英雄序号
    return num


#  根据编号获取英雄背景故事
def get_story(num):
    url = 'https://pvp.qq.com/web201605/herodetail/{}.shtml'.format(num)  # 进入英雄详细页面的链接
    res = requests.get(url=url, headers=headers)
    res.encoding = chardet.detect(res.content)['encoding']  # 统一字符编码，解决乱码问题
    res = res.text
    soup = bs4.BeautifulSoup(res, 'html.parser')
    story = soup.select('.pop-bd')[0].text  # 虚拟故事段
    story = story.replace(' ', '\n').replace('”', '\n').replace(' ', '')
    story = story.encode(encoding='utf-8')
    return story


#  下载故事
def download(hero_dream, story):  # 下载函数
    file_name = hero_dream+'.txt'
    file_path = path + '/' + file_name
    with open(file_path, 'wb') as f:
        f.write(story)
        logging.info('{}的故事已经下载完成啦！感谢您的使用~')
        f.close()


def main():
    hero_dream = input("请输入你想查看的英雄故事：")
    url = 'https://pvp.qq.com/web201605/js/herolist.json'
    num = get_hero_num(url, hero_dream)
    story = get_story(num)
    download(hero_dream, story)


if __name__ == '__main__':
    main()
