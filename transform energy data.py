# -*- coding: utf-8 -*-
"""
# @Time    : 2023/9/24 
# @Author  : Hanjiang Dong, GPT-4
# @Intro   : Hi Larissa!
"""
import numpy as np
import pandas as pd
import json

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

with open('2018_Tempe_182C_11_to_12.txt', 'r') as f:
    json_data = json.load(f)

df_columns = pd.DataFrame(json_data['columns']).iloc[:, 0]

for item in objects:
    for j in range(len(item) - 1):
        df_total = pd.DataFrame(np.nan,
                                index=pd.date_range(start='2014-01-01 00:00:00', end='2022-12-31 23:00:00', freq='H'),
                                columns=df_columns)
        for i in range(2014, 2023):
            for k in [['01', '03'], ['04', '07'], ['08', '10'], ['11', '12']]:
                with open('{num1}_{str1}_{str2}_{num2}_to_{num3}.txt'.format(str1=item[0],
                                                                             str2=item[j + 1],
                                                                             num1=i,
                                                                             num2=k[0],
                                                                             num3=k[1]), 'r') as f:
                    json_data = json.load(f)

                # df_columns = pd.DataFrame(json_data['columns']).iloc[:, 0]

                df = pd.DataFrame(json_data['rows'])

                if df.shape[0] != 0:
                    df.columns = df_columns
                    df_index = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour']])
                    df.index = df_index
                    # 使用update方法更新df2的值
                    df_total.update(df)
        df_total['campus'] = item[0]
        df_total['Year'] = df_total.index.year
        df_total['Month'] = df_total.index.month
        df_total['Day'] = df_total.index.day
        df_total['Hour'] = df_total.index.hour
        df_total['DOW'] = df_total.index.weekday
        df_total = df_total.reset_index(drop=True)
        # 保存为csv文件
        df_total.to_csv('{str1}_{str2}_{num1}_to_{num2}.csv'.format(str1=item[0],
                                                                    str2=item[j + 1],
                                                                    num1=2014,
                                                                    num2=2022), index=False)
