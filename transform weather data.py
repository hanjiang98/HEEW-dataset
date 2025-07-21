# -*- coding: utf-8 -*-
"""
# @Time    : 2023/9/29 
# @Author  : Hanjiang Dong
# @Intro   : Hi Larissa!
"""

import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

df_columns = ['Time', 'Temperature', 'Dew Point', 'Humidity', 'Wind',
              'Wind Speed', 'Wind Gust', 'Pressure', 'Precip', 'Condition']

urls = [
    'mesa',  # start_date = datetime(2020, 11, 8)
    'tempe',  # start_date = datetime(2020, 11, 8)
    'phoenix',  # start_date = datetime(2020, 11, 8)
    'glendale'  # start_date = datetime(2020, 11, 8)
]

# 定义开始和结束日期
# start_date = datetime(2020, 11, 1)
# end_date = datetime(2020, 11, 30)
start_date = datetime(2014, 1, 1)
end_date = datetime(2023, 1, 1)

# 初始化日期列表
date_list = []

# 在开始日期和结束日期之间进行迭代
delta = end_date - start_date
for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    # 将日期转化为字符串格式，并添加到列表中
    date_list.append(day.strftime('%Y-%m-%d'))

for item in urls:
    start_time = datetime(2014, 1, 1, 0, 0, 0)  # 开始日期，包括00:00:00
    end_time = datetime(2022, 12, 31, 23, 0, 0)  # 结束日期，包括23:00:00

    time_list = []
    current_time = start_time

    while current_time <= end_time:
        time_list.append(current_time.strftime('%Y-%m-%d %H:%M:%S'))
        current_time += timedelta(hours=1)

    df_total = pd.DataFrame(np.nan,
                            # index=pd.date_range(start='{str} 00:00:00'.format(str=start_date),
                            #                     end='{str} 23:00:00'.format(str=end_date), freq='H'),
                            index=time_list,
                            columns=df_columns)
    for i in range(len(date_list) - 1):
        print("reading {str1}_{str2}.txt".format(str1=item, str2=date_list[i]))
        # 读取txt文件
        # {str1}_{str2} mesa_2020-11-08
        with open("{str1}_{str2}.txt".format(str1=item, str2=date_list[i]), 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 使用列表推导式将所有包含'9:51 AM'的字符串替换为'10:00:00'
        lines = ['00:00:00' if x == '11:51 PM\n' else x for x in lines]
        lines = ['01:00:00' if x == '12:51 AM\n' else x for x in lines]
        lines = ['02:00:00' if x == '1:51 AM\n' else x for x in lines]
        lines = ['03:00:00' if x == '2:51 AM\n' else x for x in lines]
        lines = ['04:00:00' if x == '3:51 AM\n' else x for x in lines]
        lines = ['05:00:00' if x == '4:51 AM\n' else x for x in lines]
        lines = ['06:00:00' if x == '5:51 AM\n' else x for x in lines]
        lines = ['07:00:00' if x == '6:51 AM\n' else x for x in lines]
        lines = ['08:00:00' if x == '7:51 AM\n' else x for x in lines]
        lines = ['09:00:00' if x == '8:51 AM\n' else x for x in lines]
        lines = ['10:00:00' if x == '9:51 AM\n' else x for x in lines]
        lines = ['11:00:00' if x == '10:51 AM\n' else x for x in lines]
        lines = ['12:00:00' if x == '11:51 AM\n' else x for x in lines]
        lines = ['13:00:00' if x == '12:51 PM\n' else x for x in lines]
        lines = ['14:00:00' if x == '1:51 PM\n' else x for x in lines]
        lines = ['15:00:00' if x == '2:51 PM\n' else x for x in lines]
        lines = ['16:00:00' if x == '3:51 PM\n' else x for x in lines]
        lines = ['17:00:00' if x == '4:51 PM\n' else x for x in lines]
        lines = ['18:00:00' if x == '5:51 PM\n' else x for x in lines]
        lines = ['19:00:00' if x == '6:51 PM\n' else x for x in lines]
        lines = ['20:00:00' if x == '7:51 PM\n' else x for x in lines]
        lines = ['21:00:00' if x == '8:51 PM\n' else x for x in lines]
        lines = ['22:00:00' if x == '9:51 PM\n' else x for x in lines]
        lines = ['23:00:00' if x == '10:51 PM\n' else x for x in lines]

        # 逐行删除空格后面的内容，并存储到DataFrame中
        data = []
        for line in lines:
            line = line.strip()  # 删除行首和行尾的空白字符
            if ' ' in line:
                line = line.split(' ')[0]  # 以空格分割行，并保留第一个元素
            if '\xa0' in line:
                line = line.split('\xa0')[0]  # 以空格分割行，并保留第一个元素
            # line = line.split()[0]  # 以空格分割行，并保留第一个元素
            data.append(line)

        df = pd.DataFrame(data, columns=['Content'])

        if df.shape[0] != 0:
            # 将数据转换为NumPy数组，并使用reshape改变形状
            arr = np.array(data)
            reshaped_arr = arr.reshape(int(len(arr) / 10), 10)

            # 创建新的DataFrame
            index = []
            for j in range(reshaped_arr.shape[0]):
                index.append('{str1} {str2}'.format(str1=date_list[i], str2=reshaped_arr[j, 0]))
            if reshaped_arr[-1, 0] == '00:00:00':
                index[-1] = '{str1} {str2}'.format(str1=date_list[i + 1], str2=reshaped_arr[-1, 0])
            df_new = pd.DataFrame(reshaped_arr)
            # start = '{str1} {str2}'.format(str1=date_list[i], str2=df_new.iloc[0, 0])
            # end = '{str1} {str2}'.format(str1=date_list[i], str2=df_new.iloc[-1, 0])
            # # if df_new.iloc[0, 0] == '00:00:00':
            # #     start = '{str1} {str2}'.format(str1=date_list[i], str2=df_new.iloc[0, 0])
            # if df_new.iloc[-1, 0] == '00:00:00':
            #     end = '{str1} {str2}'.format(str1=date_list[i+1], str2=df_new.iloc[-1, 0])
            df_new.columns = df_columns
            # df_new.index = pd.date_range(start=start,
            #                              end=end, freq='H')
            df_new.index = index
            df_total.update(df_new)
    # 保存为csv文件
    df_total.to_csv('{str1}_weather_2014_to_2022.csv'.format(str1=item))
