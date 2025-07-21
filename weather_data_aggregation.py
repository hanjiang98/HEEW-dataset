import os
import glob
import shutil
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


def run1():
    # 要操作的列明
    cols = ["Temperature", "Dew Point", "Humidity", "Wind Speed", "Wind Gust", "Pressure", "Precip"]
    base_files = glob.glob("处理后的文件/*.csv")
    for base_file in base_files:
        filename = base_file.split('\\')[-1].split('.')[0]
        df_raw = pd.read_csv('raw data\\{}.csv'.format(filename)).drop(['Wind', 'Condition'], axis=1)
        # 读取数据的时候  -0.01 全部当作空值
        df_correction = pd.read_csv('kmeans和倍比法修正后的文件\\{}.csv'.format(filename))
        df_base = pd.read_csv(base_file)

        # 当前表的行数
        row_count = df_raw.shape[0]

        # 1.如果整列为空 全部填充0
        for col in cols:
            na_count = df_raw[col].isna().sum()
            # 如果当前列的空值==总行数 就填充0
            if na_count == row_count:
                df_raw[col] = 0

        # 如果1到N 为空   但是N+1有数值   1到N就设为0
        for col in cols:
            try:
                if df_raw[df_raw[col].isna()].index[0] == 0:
                    idx = df_raw[df_raw[col].notna()].index[0]
                    df_base[col].iloc[idx:] = df_correction[col].iloc[idx:]
                    # print(col,idx)
            except:
                pass

        df_base = df_base.reset_index(drop=True)
        df_base = df_base.round(3)
        df_base.to_csv(f'最终文件/{filename}.csv', index=False)


if __name__ == '__main__':
    shutil.rmtree('最终文件',ignore_errors=True)
    os.makedirs('最终文件', exist_ok=True)
    run1()