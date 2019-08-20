#! /usr/bin/python3
# -*- coding: utf-8 -*- 
from aip import AipSpeech
  
""" 你的 APPID AK SK """  
APP_ID = '******'
API_KEY = '******'  
SECRET_KEY = '******'  
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

vol = 12
spd = 7
pit = 7
per = 3


# s = 'master wang, please contact the administrator'
# s = 'hello, have an enjoyable day!'
# s = '二师兄不好了，师傅被抓走了'
# s = '李老师好！专属欢迎词可以定制哟'
# s = '不让你进， 就不让你进！'
# s = '大车以载， 量如江海'
# s = '你的大学，你来掌控'
# s = '山只哥，又有好玩的了'
# s = '学学人家桂红，学学人家桂红'
# s = '兹兹事体大， 尔等莫要信口胡沁'
# s = '好的，切换到工作模式'
s = '主人，请注意您的坐姿'
result  = client.synthesis(s, 'zh', 1, {
    'vol': vol,
    "spd": spd,
    "pit": pit,
    "per": per
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
if not isinstance(result, dict):
    with open('tmp.mp3', 'wb') as f:
        f.write(result)

import os
os.system('tmp.mp3')



