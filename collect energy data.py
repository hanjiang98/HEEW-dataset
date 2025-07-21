# -*- coding: utf-8 -*-
"""
# @Time    : 2023/9/18 
# @Author  : Hanjiang Dong
# @Intro   : Hi Larissa!
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import pyperclip
import time

objects = [
    ['TOTAL', 'Total'],
    ['Downtown', 'Total', '309', '305', '152A', '152B', '152C', '152D', '152F', '302', '307', '304', '308'],
    ['Polytechnic', 'Total', '004', '001', '785', '234', '827B', '795', '832', '504', '830', '571', '237', '786',
     '816', '811', '825A', '825B', '505', '826', '425', '812', '831', '632', '790', '539', '640'],
    ['Tempe', 'Total', '173B', '87', '94', '173', '104A', '104B', '104C', '39', '41', '40C', '59B', '179', '15',
     '173C', '127', '88', '135', '136', '173D', '16', '44', '6C', '53', '53G', '63', '17', '6A', '153', '11R',
     '11X', '1', '182C', '85', '160', '163', '10', '10E', '25', '173H', '2_3', '46-1', '26', '108', '75', '72',
     '173E', '56AB', '27', '61', '34', '33', '28', '40D', '37', 'MTWRP', '35', '21', '84', '86', '48', '47',
     'P03', 'P05', '6B', '57B', '13', '31', '51F', '173F', '173AN-1', '173AN-2', '173AN-3', '173AN-4', '173AS-1',
     '173AS-2', '173AS-3', '173AS-4', '55', '46', '4', '154', '5', '45', '36', '59', '162', '162D', '162A',
     '180A', '180B', '180C', '11', '150', '175', '174', '69', '49', '166', '156', '7'],
    ['West', 'Total', '905A', '905B', '916', '904', '900', '917', '901', '915', '903', '914', '902'],
]

options = webdriver.ChromeOptions()

# 处理SSL证书错误问题
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# 忽略无用的日志
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get('https://cm.asu.edu/')

# 打开新的标签页
driver.execute_script("window.open('');")

for item in objects:
    for j in range(len(item) - 1):
        for i in range(2022, 2013, -1):
            for k in [['01', '03'], ['04', '07'], ['08', '10'], ['11', '12']]:

                # 切换到新的标签页 (它是一个 0-based index)
                driver.switch_to.window(driver.window_handles[1])

                # 在新的标签页中访问另一个网站
                driver.get(
                    'https://cm.asu.edu/dgdb?db=VES&query=%5Bcm%5D.%5Bdbo%5D.%5BpCM_Retrieve_Utility_Data_By_Campus_Building%5D+%40selCampus+%3D+%22{str1}%22%2C%40selBldg+%3D+%22{str2}%22%2C%40selPeriod+%3D+%22Custom+Dates%22%2C%40selInterval+%3D+%22Hourly%22%2C%40selBeginDate+%3D+%22{num1}-{num2}-01%22%2C%40selEndDate+%3D+%22{num1}-{num3}-31%22%3B'.format(
                        str1=item[0],
                        str2=item[j + 1],
                        num1=i,
                        num2=k[0],
                        num3=k[1]))

                # driver.switch_to.window(driver.window_handles[0])
                # driver.close()

                time.sleep(10)

                # 获取页面源码
                html_source = driver.page_source

                # 使用 Beautiful Soup 解析 HTML，提取出纯文本
                soup = BeautifulSoup(html_source, 'html.parser')
                text = soup.get_text()

                # driver.find_element('#key-demo').send_keys(Keys.CONTROL, 'a')
                # driver.find_element('#key-demo').send_keys(Keys.CONTROL, 'c')
                #
                # driver.quit()
                # time.sleep(5)
                #
                # root = tk.Tk()
                # root.withdraw()  # to hide the window
                # text = root.clipboard_get()

                # 将获取到的纯文本复制到剪贴板
                pyperclip.copy(text)

                # 首先, 从剪贴板获取文本
                clipboard_text = pyperclip.paste()

                # 创建一个名为 "2014_totals" 的 txt 文档
                with open('{year}_{str1}_{str2}_{month1}_to_{month2}.txt'.format(
                        year=i,
                        str1=item[0],
                        str2=item[j + 1],
                        month1=k[0],
                        month2=k[1]), 'w',
                          encoding='utf-8') as f:
                    # 将剪贴板的文本写入 txt 文档
                    f.write(clipboard_text)

                time.sleep(2)

                # 关闭当前的标签页
                # driver.switch_to.window(driver.window_handles[-1])
                # driver.close()

                # # 回到原来的标签页
                # driver.switch_to.window(driver.window_handles[0])

# 校区的
'https://cm.asu.edu/dgdb?db=VES&query=%5Bcm%5D.%5Bdbo%5D.%5BpCM_Retrieve_Utility_Data_By_Campus_Building%5D+%40selCampus+%3D+%22TOTAL%22%2C%40selBldg+%3D+%22Total%22%2C%40selPeriod+%3D+%22Custom+Dates%22%2C%40selInterval+%3D+%22Hourly%22%2C%40selBeginDate+%3D+%222014-01-01%22%2C%40selEndDate+%3D+%222014-12-31%22%3B'
'https://cm.asu.edu/dgdb?db=VES&query=%5Bcm%5D.%5Bdbo%5D.%5BpCM_Retrieve_Utility_Data_By_Campus_Building%5D+%40selCampus+%3D+%22Downtown%22%2C%40selBldg+%3D+%22Total%22%2C%40selPeriod+%3D+%22Custom+Dates%22%2C%40selInterval+%3D+%22Hourly%22%2C%40selBeginDate+%3D+%222014-01-01%22%2C%40selEndDate+%3D+%222014-12-31%22%3B'
'https://cm.asu.edu/dgdb?db=VES&query=%5Bcm%5D.%5Bdbo%5D.%5BpCM_Retrieve_Utility_Data_By_Campus_Building%5D+%40selCampus+%3D+%22Downtown%22%2C+%40selBldg+%3D+%22152A%22%2C%40selPeriod+%3D+%22Custom+Dates%22%2C%40selInterval+%3D+%22Hourly%22%2C%40selBeginDate+%3D+%222017-01-01%22%2C%40selEndDate+%3D+%222017-12-31%22%3B'
# 楼栋的

# 房间的


# # 在新的标签页中访问另一个网站
# driver.get('http://www.google.com')
#
# # 获取页面的源代码
# content = driver.page_source
#
# print(content)
#
# print(content)
