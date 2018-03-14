#-*- coding:utf-8 -*-
from WechatSprider.MySprider import WechatSprider
if __name__ == '__main__':
   ws=WechatSprider('yzhang9mail@gmail.com',"zhangyan123","C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",'电动汽车')
   # ws.login_weixin()
   # maxnum=ws.search_total() #得到了总数之后建议切片做搜索
   # ws.get_user(0,50,'0_50.json')
   # ws.get_link('./data/userfile/userfile0_50.json','./data/linkfile/linkfile0_50.json',2)
   ws.get_content('./data/linkfile/linkfile0_50.json','./result/result0_50.json')