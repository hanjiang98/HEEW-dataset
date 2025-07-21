# -*- coding: utf-8 -*-
"""
# @Time    : 2023/9/25 
# @Author  : Hanjiang Dong
# @Intro   : Hi Larissa!
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta


def scrape_data(url, date):
    options = webdriver.ChromeOptions()

    # 处理SSL证书错误问题
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    # 忽略无用的日志
    options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    driver = webdriver.Chrome(options=options)

    # 打开指定的网页
    driver.get('https://www.wunderground.com/history/daily/us/az/{str1}/KPHX/date/{str2}'.format(str1=url, str2=date))

    time.sleep(4)

    # 获取网页的HTML内容
    html = driver.page_source

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html, 'html.parser')

    # 找到所有的表格
    tables = soup.find_all('table')

    # 尝试获取第二个表格的数据
    try:
        # 以utf-8编码打开一个新的文本文件并写入第二个表格的数据
        with open('{str1}_{str2}.txt'.format(str1=url, str2=date), 'w', encoding='utf-8') as f:
            for row in tables[1].find_all('tr'):
                columns = row.find_all('td')
                for column in columns:
                    f.write(column.get_text() + '\n')
        print("saved {str1}_{str2}.txt".format(str1=url, str2=date))
        time.sleep(1)
        # 关闭浏览器窗口
        # driver.quit()
    except IndexError:
        print("IndexError occurred. Retrying...")
        # driver.quit()
        time.sleep(1)  # 等待5秒钟以避免过于频繁的请求
        scrape_data(url, date)


urls = [
    'mesa',  # start_date = datetime(2020, 11, 8)
    'tempe',  # start_date = datetime(2020, 11, 8)
    'phoenix',  # start_date = datetime(2020, 11, 8)
    'glendale'  # start_date = datetime(2020, 11, 8)
]

# 定义开始和结束日期
start_date = datetime(2013, 12, 31)
# start_date = datetime(2014, 1, 1)
end_date = datetime(2022, 12, 31)


# 初始化日期列表
date_list = []

# 在开始日期和结束日期之间进行迭代
delta = end_date - start_date
for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    # 将日期转化为字符串格式，并添加到列表中
    date_list.append(day.strftime('%Y-%m-%d'))

# 开始爬取数据
for url in urls:
    for date in date_list:
        scrape_data(url, date)
