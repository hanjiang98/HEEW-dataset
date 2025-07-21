# -*- coding: utf-8 -*-
"""
# @Time    : 2023/9/29 
# @Author  : Hanjiang Dong
# @Intro   : Hi Larissa!
"""
import pandas as pd

urls = [
    'mesa',  # start_date = datetime(2020, 11, 8)
    'tempe',  # start_date = datetime(2020, 11, 8)
    'phoenix',  # start_date = datetime(2020, 11, 8)
    'glendale'  # start_date = datetime(2020, 11, 8)
]

names = [
    'CN02',
    'CN03',
    'CN01',
    'CN04'
]

for i in range(len(urls)):
    df = pd.read_csv('{str1}_weather_2014_to_2022.csv'.format(str1=urls[i]), index_col=0)
    df.index = pd.date_range(start='2014-01-01 00:00:00', end='2022-12-31 23:00:00', freq='H')
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df['Day'] = df.index.day
    df['Hour'] = df.index.hour
    df['DOW'] = df.index.weekday
    df = df.reset_index(drop=True)

    # 获取DataFrame的列名
    columns = df.columns.tolist()

    # 将最后三列数据移到最前面
    new_columns = columns[-5:] + columns[1:-5]
    df = df.reindex(columns=new_columns)

    df.to_csv('{str}_weather.csv'.format(str=names[i]), index=False)


