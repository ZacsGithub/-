# -*- coding: UTF-8 -*-
"""
@Author  ：远方的星
@Time   : 2021/3/20 7:44
@CSDN    ：https://blog.csdn.net/qq_44921056
@腾讯云   ： https://cloud.tencent.com/developer/column/91164
"""
from fake_useragent import UserAgent
import requests
from lxml import etree
import bs4
import os
# 创建一个文件夹来报预保存图片
if not os.path.exists('D:/Animex动漫社'):
    os.mkdir('D:/Animex动漫社')
# 创建随机请求头
ua = UserAgent(verify_ssl=False, path='fake_useragent.json')
# 用户输入爬取的页数
page = input('请输入想要爬取的页数')
page = int(page) + 1
# 使用for循环进行多页爬取
for i in range(1, page):
    url = 'http://www.animetox.com/category/pic/pixiv/page/{}'.format(i)
    # 获取页面内容
    response_1 = requests.get(url).text
    html = etree.HTML(response_1)
    image_urls = html.xpath('//*[@id="main-contents"]/section[2]/div/div/article')  # 找到各个article节点
    for j in range(len(image_urls)):
        # 提取每一组的图片的访问链接
        image_url = image_urls[j].xpath('./a/@href')[0]
        # 获取页面内容
        response_2 = requests.get(image_url).text
        html = response_2
        soup = bs4.BeautifulSoup(html, 'html.parser')
        # 获取指定的节点，排除掉p节点的干扰项
        image_src_s = soup.select('.cps-post-main-box div p[style="text-align: center;"]')
        # 定义num方便图片命名
        num = 1
        for k in range(len(image_src_s)):
            # 获取指定节点下的节点
            image_src = image_src_s[k].select('img')
            # 即使排除了干扰项，但可能存在满足条件，但内容为空的情况，于是使用条件循环进行筛选
            if image_src == []:
                continue
            else:
                image_src = image_src[0]
            # 获取图片链接
            image_src = image_src.get('data-lazy-src')
            # 得到图片内容
            image_data = requests.get(image_src).content
            # 图片名字
            image_name = '{}_{}_{}.jpg'.format(i, j+1, num)
            # 图片保存小路径名字
            path_name = '{}_{}'.format(i, j+1)
            # 大路径名字
            path = 'D:/Animex动漫社/' + path_name
            if not os.path.exists(path):
                os.mkdir(path)
            # 图片的保存路径
            image_path = path + '/' + image_name
            num += 1
            # 保存文件
            with open(image_path, 'wb') as f:
                f.write(image_data)
                print(image_name, '下载成功！')
                f.close()
