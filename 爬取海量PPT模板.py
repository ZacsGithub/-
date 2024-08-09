# -*- coding: UTF-8 -*-
"""
@Author  ：远方的星
@Time   : 2021/5/4 21:17
@CSDN    ：https://blog.csdn.net/qq_44921056
@腾讯云   ： https://cloud.tencent.com/developer/column/91164
"""
import os
import chardet
import requests
import logging
from lxml import etree
from tqdm import tqdm
from fake_useragent import UserAgent

# 日志输出的基本配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# 随机产生请求头
ua = UserAgent(verify_ssl=False, path='fake_useragent.json')

path = 'D:/PPT模板'
if not os.path.exists(path):
    os.mkdir(path)


# 随机切换请求头
def random_ua():
    headers = {
        "accept-encoding": "gzip",    # gzip压缩编码  能提高传输文件速率
        "user-agent": ua.random
    }
    return headers


# 得到xpath对应的结果
def get_link(url, xpath):
    response = requests.get(url=url, headers=random_ua())
    response.encoding = chardet.detect(response.content)['encoding']  # 自动转换编码格式，与网页一致
    response = response.text
    html = etree.HTML(response)
    link = html.xpath(xpath)
    return link


# 获取下载链接并下载
def get_zip_url(url):
    xpath_1 = '/html/body/div[2]/ul/li'
    xpath_2 = '/html/body/div[2]/div[2]/div/div[1]/div[2]/a/@href'
    xpath_3 = '/html/body/div[1]/div/ul/li[1]/a/@href'
    a = get_link(url, xpath_1)  # 获取所有的li节点
    for i in tqdm(range(len(a))):  # 对li节点进行遍历
        webpage_url = 'https://www.ypppt.com' + a[i].xpath('./a[1]/@href')[0]  # 获取到第一个链接
        zip_name = a[i].xpath('./a[2]/text()')[0] + '.zip'  # 获取文本，组成待下载文件的文件名
        download_link = 'https://www.ypppt.com' + get_link(webpage_url, xpath_2)[0]  # 获取下载页面
        download_url = get_link(download_link, xpath_3)[0]  # 获取下载链接
        save_path = path + '/' + zip_name  # 图片的保存地址
        res = requests.get(url=download_url, headers=random_ua()).content
        with open(save_path, 'wb') as f:  # 写入文件，即下载
            f.write(res)


def main():
    page = int(input('请输入你想要爬取的页数：'))
    # 网页第一页和之后的地址不是同一个规律，使用条件判断
    for num in range(1, page+1):
        if num == 1:
            url = 'https://www.ypppt.com/moban/'
            logging.info('正在下载第1页模板，请稍等片刻嗷')
            get_zip_url(url)
        else:
            url = 'https://www.ypppt.com/moban/list-{}.html'.format(num)
            logging.info('正在下载第{}页模板，请稍等片刻嗷'.format(num))
            get_zip_url(url)
    logging.info('你所要求的任务，全部都完成喽~')


if __name__ == "__main__":
    main()
