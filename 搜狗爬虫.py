# -*- coding: utf-8 -*-
import os
import random
import re
import subprocess
import time
from urllib import parse
import faker
import requests
import urllib3
import xlwt
import xlrd
from lxml import etree
from ip import get_ip
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

urllib3.disable_warnings()

key_ls = ["chatgpt", "chatgpt聊天机器人", "chatgpt 智能机器人","chatgpt智能问答平台","chatgpt机器人","chatgpt AI", "Chatgpt人工智能"]

def get_sg_info(key, content_list):
    ip_ls = get_ip()
    for num in range(1,11):
        for x in range(3):
            try:
                headers = {
                    "User-Agent": faker.Factory.create().user_agent()}
                url = 'https://weixin.sogou.com/weixin?query={}&_sug_type_=&s_from=input&_sug_=n&type=2&page={}&ie=utf8'.format(parse.quote(key), num)
                r = requests.get(url, headers=headers, verify=False, proxies=ip_ls)
                r_element = etree.HTML(r.content.decode())
                news_list = r_element.xpath('//ul[@class="news-list"]/li/div[2]')
                if r.status_code != 200 and  not news_list:
                    ip_ls = get_ip()
                for news in news_list:
                    news_href = "".join(news.xpath('./h3/a/@href'))
                    news_href = news_href if not news_href.startswith('/') else 'https://weixin.sogou.com' + news_href
                    news_title = "".join("".join(news.xpath('./h3//text()')).split())
                    news_author = "".join(news.xpath('./div/a/text()'))
                    news_time = "".join(news.xpath('./div/span/script/text()'))
                    news_time = re.search(r'\d{5,20}', news_time).group()
                    news_time = time.strftime("%Y-%m-%d", time.localtime(int(news_time)))
                    news_detali,ip_ls = get_detail(news_href, ip_ls)
                    con_ls = ["".join(x.split()) for x in [news_title, news_author,news_time, news_href, key, news_detali]]
                    content_list.append(con_ls)
                    print(con_ls)
                time.sleep(random.randint(2,3))
                break
            except Exception as e:
                print(e)
                ip_ls = get_ip()
    return content_list


def get_detail(news_href, ip_ls):
    for x in range(3):
        try:
            headers = {
                "Host": "weixin.sogou.com",
                "Cookie": "ABTEST=3|1676536160|v1; IPLOC=CN3100; SUID=4917E974BA18960A0000000063EDE960; SUID=4917E9743320B00A0000000063EDE960; SUV=0034B52374E9174963EDE960E9AF1191; JSESSIONID=aaaF16U70DzQw8XIvP7vy; PHPSESSID=llq44s831rrn9efd0dhh2kjhn6; SNUID=F0AE50CDBABC4D5B1950FCD9BAA0084B",
                "User-Agent": faker.Factory.create().user_agent()}
            r = requests.get(news_href, headers=headers, proxies=ip_ls).text
            v = re.findall(r"url \+= '(.+?)';", r)
            v = "".join(v).replace('@', '')
            print(v)
            headers  ={
                "User-Agent": faker.Factory.create().user_agent()
            }
            r2 = requests.get(v, headers=headers, proxies=ip_ls)
            r_element = etree.HTML(r2.content.decode())
            news_list = r_element.xpath('//div[@id="js_content"]//text()')
            return "".join(news_list), ip_ls
        except Exception as e:
            print(e)
            ip_ls = get_ip()


def write_file(content_dict):
    # 指定file以utf-8的格式打开
    file = xlwt.Workbook(encoding='utf-8')
    # 指定打开的文件名
    table = file.add_sheet('Shell1', cell_overwrite_ok=True)
    info_list = [['标题', '作者', '发布时间', '链接', '关键词','正文']] + content_dict
    for i, p in enumerate(info_list):
        # 将数据写入文件,i是enumerate()函数返回的序号数
        for j, q in enumerate(p):
            # print(i, j, q)
            table.write(i, j, q)
    file.save('新闻.xls')


def run():
    content_list = []
    for key in key_ls:
        content_list = get_sg_info(key, content_list)
    write_file(content_list)


if __name__ == '__main__':
    run()
    # print(get_detail("https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7dMdfcaKSsZBOtnbN8VDyvMAygv2XCDvlqXa8Fplpd99GTUYEoryjAsjxxIh9K3_SK2AbjD6UWyWFw4DJdRtYxdIsbO8bbI2vaw-WmNx1FXy-vg0-06_Ug_pbgGbmJGeUzPineya0M-Iop2tk1vUqF4y7d0BjdTxVxZTYySiMguoNsSMcCEGQjC3sfYwP9V_PE94y_7gZjYjODLYKb-Cjyfxjh3za6jWA..&type=2&query=chatgpt&token=BA0FFAFAF0AE50CDBABC4D5B1950FCD9BAA0084B63F33A5D&k=32&h=7"))