# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 18:50:58 2019

@author: Administrator
"""

from wxpy import *

bot = Bot()
bot.enable_puid('wxpy_puid.pkl')
my_friend = bot.friends().search('忆文')[0]
print(my_friend.puid)
my_friend.send('Hello, WeChat!')
bot.file_helper.send('Hello from wxpy!')

