# -*- coding: UTF-8 -*-
"""
@Author  ：远方的星
@Time   : 2021/4/18 21:26
@CSDN    ：https://blog.csdn.net/qq_44921056
@腾讯云   ： https://cloud.tencent.com/developer/column/91164
"""

import os
import cv2
import requests
from tqdm import tqdm
from lxml import etree
from mutagen.mp3 import MP3
from moviepy.editor import VideoFileClip, AudioFileClip


headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
path = 'D:/test/tupian'
if not os.path.exists(path):
    os.mkdir(path)


#  爬取阴阳师图片
def get_picture(url, num_1, num_2):
    response = requests.get(url=url, headers=headers).text
    html = etree.HTML(response)
    lists = html.xpath('/html/body/div[2]/div[3]/div[1]/div[3]/div[2]/div')
    num = 0
    for i in tqdm(range(num_1, num_2)):  # tqdm的作用是加上进程进度条
        a = lists[i].xpath('./div/div/a[contains(text(), "1920x1080")]')  # 根据文本内容锁定节点a
        if a == []:  # 有些图片的分辨率较少，需要加上条件筛选
            num += 1
        else:
            image_url = a[0].xpath('./@href')[0]  # 获取原画壁纸链接
            image_data = requests.get(url=image_url).content
            image_name = '{}.jpg'.format(num)  # 给每张图片命名
            save_path = path + '/' + image_name  # 图片的保存地址
            with open(save_path, 'wb') as f:
                f.write(image_data)
                f.close()
                num += 1


# 合成视频
def get_video(num_1, num_2):
    video_dir = 'D:/test/result.mp4'      # 输出视频的保存路径
    fps = 1      # 帧率
    img_size = (1920, 1080)      # 图片尺寸
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)
    for i in tqdm(range(num_1, num_2)):
        img_path = 'D:/test/tupian/' + '{}.jpg'.format(i)
        frame = cv2.imread(img_path)
        frame = cv2.resize(frame, img_size)  # 生成视频   图片尺寸和设定尺寸相同
        videoWriter.write(frame)  # 将图片写进视频里
    videoWriter.release()  # 释放资源


# 加入音频
def get_audio():
    videoFile = 'D:/test/result.mp4'  # 视频文件
    video = VideoFileClip(videoFile)
    videos = video.set_audio(AudioFileClip('D:/hlh.mp3'))  # 音频文件
    videos.write_videofile('D:/test/sound.mp4', audio_codec='aac')  # 保存合成视频，注意加上参数audio_codec='aac'，否则音频无声音


# 计算每个音频的时间（秒）
def get_time_count():
    audio = MP3("D:/hlh.mp3")
    time_count = int(audio.info.length)
    return time_count


def main():
    base_url = 'https://yys.163.com/media/picture.html'
    num_1 = 0
    num_2 = get_time_count()
    print('开始爬取阴阳师插画，请稍等片刻')
    get_picture(base_url, num_1, num_2)
    print('图片正在整和成视频，请稍后片刻')
    get_video(num_1, num_2)
    print('正在给视频加入音频')
    get_audio()
    print('恭喜你，完整的视频已经生成了！！！')


if __name__ == '__main__':
    main()
