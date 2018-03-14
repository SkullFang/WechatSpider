#-*- coding:utf-8 -*-
from selenium import webdriver
import time
import json
import requests
import time
import re
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
class WechatSprider:

    def __init__(self,username,password,chrome_path,keyword):
        """
        :param username:  公众号账号
        :param password:  公众号密码
        :param chrome_path: chromedriver path
        """
        self.username=username
        self.password=password
        self.chrome_path=chrome_path
        self.keyword=keyword

    def login_weixin(self,cookiesfile='./data/cookies.json'):
        """
        登陆微信公众号在data目录下生成用户的cookies文件
        :return:
        """
        # driver
        driver = webdriver.Chrome(self.chrome_path)
        driver.get("https://mp.weixin.qq.com/")
        # login
        driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/form/div[1]/div[1]/div/span/input').clear()
        driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/form/div[1]/div[1]/div/span/input').send_keys(
            self.username)

        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/form/div[1]/div[2]/div/span/input').clear()
        driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/form/div[1]/div[2]/div/span/input').send_keys(
            self.password)
        time.sleep(2)

        driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/form/div[3]/label').click()
        time.sleep(2)

        driver.find_element_by_xpath('//*[@id="header"]/div[2]/div/div/form/div[4]/a').click()

        time.sleep(20)
        cookies = driver.get_cookies()  # get cookies

        cookie = {}
        for items in cookies:
            cookie[items.get('name')] = items.get('value')

        # save cookies file
        with open(cookiesfile, 'w') as file:
            file.write(json.dumps(cookie,indent=4))

        driver.close()

    def search_total(self,cookiefile='./data/cookies.json'):
        with open(cookiefile, 'r') as file:
            cookie = file.read()

        url = 'https://mp.weixin.qq.com/'
        cookies = json.loads(cookie)

        response = requests.get(url, cookies=cookies)

        token = re.findall(r'token=(\d+)', str(response.url))[0]

        data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'query': self.keyword,
            'begin': '5',
            'count': '5'
        }
        get_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&'

        headers = {
            'User-Agent': "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=359957400&lang=zh_CN',
            'X-Requested-With': 'XMLHttpRequest'
        }

        search_response = requests.get(get_url, headers=headers, cookies=cookies, params=data)
        rep_json = search_response.json()
        max_num=rep_json.get('total')
        return max_num

    def get_user(self,start,end,downfile,cookiefile='./data/cookies.json'):
        with open(cookiefile, 'r') as file:
            cookie = file.read()

        url = 'https://mp.weixin.qq.com/'
        cookies = json.loads(cookie)

        response = requests.get(url, cookies=cookies)

        token = re.findall(r'token=(\d+)', str(response.url))[0]

        get_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&'

        headers = {
            'User-Agent': "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=359957400&lang=zh_CN',
            'X-Requested-With': 'XMLHttpRequest'
        }

        max_num = end

        proxies = {
            'ip_port': 'proxy.tyo.sap.corp:8080',

        }

        begin = start
        relist = []
        result_dir = {}
        while begin < max_num:
            data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'query': self.keyword,
                'begin': '{}'.format(str(begin)),
                'count': '5'
            }
            search_response = requests.get(get_url, headers=headers, cookies=cookies, params=data, proxies=proxies)
            rep_json = search_response.json()
            content = rep_json.get('list')

            for items in content:
                print(items.get('nickname'))
                print(items.get('fakeid'))

                result_dir[items.get('nickname')] = items.get('fakeid')

                relist.append(str(items.get('nickname')))

            begin = int(begin)
            print(begin)
            begin = begin + 5
            time.sleep(random.randint(8, 15))

        for item in result_dir:
            print(item)

        d_file = './data/userfile/' + downfile
        with open(d_file, 'w', encoding='utf8') as file:
            file.write(json.dumps(result_dir, ensure_ascii=False, indent=4))

    def get_link(self,inputfile,outputfile,number):
        with open("./data/cookies.json", 'r') as file:
            cookie = file.read()

        print(cookie)

        with open(inputfile, 'r', encoding='utf-8') as file:
            user_info = json.load(file)

        users = []
        fakeids = []
        for k, v in user_info.items():
            users.append(k)
            fakeids.append(v)

        url = 'https://mp.weixin.qq.com/'
        cookies = json.loads(cookie)

        response = requests.get(url, cookies=cookies)

        token = re.findall(r'token=(\d+)', str(response.url))[0]

        result_dir = {}

        for i in range(number):
            fakeid = fakeids[i]

            header = {
                'User-Agent': "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
                'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=359957400&lang=zh_CN',
                'X-Requested-With': 'XMLHttpRequest'
            }

            query_id_data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '0',
                'count': '5',
                'query': '',
                'fakeid': fakeid,
                'type': '9'
            }
            appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
            appmsg_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            max_num = appmsg_response.json().get('app_msg_cnt')
            # num = int(int(max_num) / 5)
            num = 5
            print(num)
            begin = 0
            relist = []
            while num + 1 > 0:
                query_id_data = {
                    'token': token,
                    'lang': 'zh_CN',
                    'f': 'json',
                    'ajax': '1',
                    'random': random.random(),
                    'action': 'list_ex',
                    'begin': '{}'.format(str(begin)),
                    'count': '5',
                    'query': '',
                    'fakeid': fakeid,
                    'type': '9'
                }
                print('翻页###################', begin)
                query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
                fakeid_list = query_fakeid_response.json().get('app_msg_list')
                for item in fakeid_list:
                    print(item.get('link'))
                    relist.append(item.get('link'))

                num -= 1
                begin = int(begin)
                begin += 5
                time.sleep(random.randint(10, 20))

            result_dir[users[i]] = relist

        with open(outputfile, 'w', encoding='utf8') as file:
            file.write(json.dumps(result_dir, ensure_ascii=False, indent=4))

    def get_content(self,inputfile,outputfile):

        with open(inputfile, 'r', encoding='utf-8') as file:
            user_info = json.load(file)

        dir_name = {}
        for k in user_info:
            name = k
            li_name = []
            try:
                for link in user_info[name]:
                    print(link)
                    result_dir = {}
                    resp = urlopen(link).read()
                    soup = BeautifulSoup(resp, 'html.parser')

                    # 获取标题

                    title = soup.find('h2', {'class', 'rich_media_title'}).string
                    title = title.strip()
                    result_dir['title'] = title
                    # print(title)

                    # 获取时间
                    time = soup.find('em', {'class', 'rich_media_meta rich_media_meta_text'}).get_text()
                    result_dir['time'] = time
                    # print(time)

                    # 获取内容
                    contents = soup.find('div', {'class', 'rich_media_content'}).findAll('span')
                    con_list = []

                    for content in contents:
                        if content.string is not None:
                            con_list.append(content.string)

                    con_str = ''.join(con_list)
                    # print(con_str)
                    result_dir['content'] = con_str
                    # print(result_dir)
                    li_name.append(result_dir)
            except:
                dir_name[name] = li_name
                continue
            finally:
                dir_name[name]=li_name

        with open(outputfile, 'w', encoding='utf8') as file:
            file.write(json.dumps(dir_name, ensure_ascii=False, indent=4))