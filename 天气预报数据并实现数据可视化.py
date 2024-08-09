# -*- coding: UTF-8 -*-
"""
@Author  ：远方的星
@Time   : 2021/2/28 10:20
@CSDN    ：https://blog.csdn.net/qq_44921056
@腾讯云   ： https://cloud.tencent.com/developer/column/91164
"""
import requests
from lxml import etree
from fake_useragent import UserAgent
import pandas as pd
from matplotlib import pyplot as plt

# 随机产生请求头
ua = UserAgent(verify_ssl=False, path='fake_useragent.json')


# 获取七天和八到十五天的页面链接
def get_url(url):
    response = requests.get(url=url).text
    html = etree.HTML(response)
    url_7 = 'http://www.weather.com.cn/' + html.xpath('//*[@id="someDayNav"]/li[2]/a/@href')[0]
    url_8 = 'http://www.weather.com.cn/' + html.xpath('//*[@id="someDayNav"]/li[3]/a/@href')[0]
    return url_7, url_8


# 获取未来七天天起预报数据
def get_data_1(url):
    response = requests.get(url=url)
    response.encoding = "utf-8"  # 防止乱码，进行编码
    response = response.text
    html = etree.HTML(response)
    list_s = html.xpath('//*[@id="7d"]/ul/li')
    # 提前定义五个空列表用于存放信息
    data, weather, x, y, wind_scale = [], [], [], [], []
    temperature = []  # 定义一个空列表，用于处理最低气温和最高气温的合并
    wind = []  # 定义一个空列表，用于存放风向
    high, low = [], []  # 定义两个空列表，用于存放未处理的最高、最低气温，为绘图做铺垫
    for i in range(len(list_s)):
        a = list_s[i].xpath('./h1/text()')  # 获取日期
        b = list_s[i].xpath('./p[1]/text()')  # 获取天气情况
        c = list_s[i].xpath('./p[2]/span/text()')  # 获取最高气温
        d = list_s[i].xpath('./p[2]/i/text()')  # 获取最低气温
        g = list_s[i].xpath('./p[3]/i/text()')  # 获取风级
        data.append(''.join(a))  # 集中日期
        weather.append(''.join(b))  # 集中天气情况
        high.append(''.join(c))  # 集中最高气温
        low.append(''.join(d))  # 集中最低气温
        x.append(''.join(c))  # 集中最高气温
        x.append('/')  # 加入一个分隔符
        x.append(''.join(d))  # 集中最低气温
        temperature.append(''.join(x[0:3]))  # 把最高气温和最低气温合并
        wind_scale.append(''.join(g))  # 集中风级
        f = list_s[i].xpath('./p[3]/em/span/@title')  # 获取风向
        if f[0] == f[1]:  # 条件语句，用于判断两个风向是否一致，进而做出一定反应
            wind.append(''.join(f[0]))
        else:
            y.append(''.join(f[0]))
            y.append('转')
            y.append(''.join(f[1]))
            wind.append(''.join(y[0:3]))
    excel = pd.DataFrame()  # 定义一个二维表
    excel['日期'] = data
    excel['天气'] = weather
    excel['气温'] = temperature
    excel['风向'] = wind
    excel['风级'] = wind_scale
    excel['最高气温'] = high
    excel['最低气温'] = low
    return excel


# 获取8-15天天气预报数据
def get_data_2(url):
    response = requests.get(url=url)
    response.encoding = "utf-8"  # 防止乱码，进行编码
    response = response.text
    html = etree.HTML(response)
    list_s = html.xpath('//*[@id="15d"]/ul/li')
    # 提前定义五个空列表用于存放信息
    data, weather, a, wind, wind_scale = [], [], [], [], []
    temperature = []  # 定义一个空列表，用于处理最低气温和最高气温的合并
    high, low = [], []  # 定义两个空列表，用于存放未处理的最高、最低气温，为绘图做铺垫
    for i in range(len(list_s)):
        data_s = list_s[i].xpath('./span/text()')  # data_s[0]是日期，data_s[1]是天气，data_s[2]是最低气温，data_s[3]是风向，data_s[4]是风级
        b = list_s[i].xpath('./span/em/text()')  # 获得最高气温
        data.append(''.join(data_s[0]))  # 集中日期
        weather.append(''.join(data_s[1]))  # 集中天气
        wind.append(''.join(data_s[3]))  # 集中风向
        wind_scale.append(''.join(data_s[4]))  # 集中风级
        high.append(''.join(b))  # 集中最高气温
        low.append(''.join(data_s[2]))  # 集中最低气温
        a.append(''.join(b))  # 集中最高气温
        a.append(''.join(data_s[2]))  # 集中最低气温（这时最高气温已经在a列表里了）
        temperature.append(''.join(a[0:2]))  # 集中最低+最高气温
    excel = pd.DataFrame()  # 定义一个二维表
    excel['日期'] = data
    excel['天气'] = weather
    excel['气温'] = temperature
    excel['风向'] = wind
    excel['风级'] = wind_scale
    excel['最高气温'] = high
    excel['最低气温'] = low
    return excel


# 实现数据可视化
def get_image(data, high, low):
    # 用来正常显示中文标签
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 用来正常显示负号
    plt.rcParams['axes.unicode_minus'] = False
    # 根据数据绘制图形
    fig = plt.figure(dpi=128, figsize=(10, 6))
    plt.plot(data, high, c='red', alpha=0.5)
    plt.plot(data, low, c='blue', alpha=0.5)
    # 给图表中两条折线中间的部分上色
    plt.fill_between(data, high, low, facecolor='blue', alpha=0.2)
    # 设置图表格式
    plt.title('北京近15天天气预报', fontsize=24)
    plt.xlabel('日期', fontsize=12)
    # 绘制斜的标签，以免重叠
    fig.autofmt_xdate()
    plt.ylabel('气温', fontsize=12)
    # 参数刻度线设置
    plt.tick_params(axis='both', which='major', labelsize=10)
    # 修改刻度
    plt.xticks(data[::1])
    # 显示图片
    plt.show()


def main():
    url = 'http://www.weather.com.cn/weather1d/101010100.shtml'
    url_7, url_8 = get_url(url)
    data_1 = get_data_1(url_7)
    data_2 = get_data_2(url_8)
    data_s = pd.concat([data_1, data_2], axis=0)
    data_s['最高气温'] = data_s['最高气温'].map(lambda z: int(z.replace('℃', '')))
    data_s['最低气温'] = data_s['最低气温'].map(lambda z: int(z.replace('℃', '').replace('/', '')))
    # print(type(data_s))
    # print(type(data_s['最高气温']))   # 有兴趣的小伙伴，可以看一下这里的类型分析嗷，这两个数据是不一样哒
    data = data_s['日期']
    high = data_s['最高气温']
    low = data_s['最低气温']
    get_image(data, high, low)


if __name__ == '__main__':
    main()
