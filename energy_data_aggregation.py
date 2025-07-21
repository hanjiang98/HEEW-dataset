import os
import glob
import shutil
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


def run1():
    def func1(v):
        if v <= -0.01:
            return np.nan
        return v
    # 要操作的列明
    cols = ["Electricity", "PV", "Cooling", "Heat"]
    base_files = glob.glob("处理后的文件/*.csv")
    for base_file in base_files:
        filename = base_file.split('\\')[-1].split('.')[0]
        df_raw = pd.read_csv('raw data\\{}.csv'.format(filename))
        # 读取数据的时候  -0.01 全部当作空值
        df_raw = df_raw.applymap(func1)
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
        df_base['Total Energy'] = df_base['Electricity']*3.41/1000 + df_base['Cooling']*3.41/0.284/1000 + df_base['Heat']
        df_base['Total Energy'] = df_base['Total Energy']
        df_base['Emission'] = (df_base['Total Energy']*1000/3.41-df_base['PV'])/1000/2204.62*(1191.35+0.01913*21+0.01558*310)
        df_base['Emission'] = df_base['Emission']
        df_base = df_base.round(3)
        df_base.to_csv(f'最终文件/{filename}.csv', index=False)


def run2():
    df_dict = {
        "CN01": [1, 11],
        "CN02": [12, 36],
        "CN03": [37, 136],
        "CN04": [137, 147],
    }

    for idx, lis in df_dict.items():
        df_res = pd.read_csv(f"最终文件\\BN001_energy.csv").set_index(
            ["Year", "Month", "Day", "Hour", "Weekday"]).applymap(lambda x: 0)
        start = lis[0]
        end = lis[1]
        for num in range(start, end + 1):
            num = str(num).zfill(3)
            filename = f'最终文件\\BN{num}_energy.csv'
            df = pd.read_csv(filename).set_index(["Year", "Month", "Day", "Hour", "Weekday"])
            # print(df.shape)

            try:
                df_res += df
            except:
                print(filename)
        df_res = df_res.round(3)
        df_res.reset_index().to_csv(f'最终文件/{idx}_energy.csv', index=False)

    df_res2 = pd.read_csv(f"最终文件\\CN01_energy.csv").set_index(
        ["Year", "Month", "Day", "Hour", "Weekday"]).applymap(lambda x: 0)
    for idx, lis in df_dict.items():
        num = str(idx).zfill(2)
        filename = f'最终文件\\{num}_energy.csv'
        df = pd.read_csv(filename).set_index(["Year", "Month", "Day", "Hour", "Weekday"])
        try:
            df_res2 += df
        except:
            print(filename)
    df_res2 = df_res2.round(3)
    df_res2.reset_index().to_csv(f'最终文件/Total_energy.csv', index=False)


if __name__ == '__main__':
    shutil.rmtree('最终文件',ignore_errors=True)
    os.makedirs('最终文件', exist_ok=True)
    run1()
    run2()