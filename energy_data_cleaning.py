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
    cols = ["Electricity", "PV", "Cooling", "Heat", "Emission"]
    base_files = glob.glob("raw data/*.csv")  # ["raw data\\BN147_energy.csv"]
    df_statistics = pd.DataFrame()
    for base_file in base_files:
        print(base_file)
        filename = base_file.split('\\')[-1].split('.')[0]
        # J 列不要
        df_base = pd.read_csv(base_file).drop('Total Energy', axis=1)
        # 读取数据的时候  -0.01 全部当作空值
        df_base = df_base.applymap(func1)
        # 当前表的行数
        row_count = df_base.shape[0]

        # 1.如果整列为空 全部填充0
        for col in cols:
            na_count = df_base[col].isna().sum()
            # 如果当前列的空值==总行数 就填充0
            if na_count == row_count:
                df_base[col] = -1
            else:
                try:
                    if df_base[df_base[col].isna()].index[0] == 0:
                        idx = df_base[df_base[col].notna()].index[0]
                        df_base[col].iloc[0:idx] = -1
                        # print(col,idx)
                except:
                    pass

                col_list = df_base[col].dropna().tolist()
                # 获得该列的上四分数*5的值
                max_val = np.percentile(col_list, 75) * 5
                series = df_base[col]
                # 将大于的值 填充为outlier
                series[series > max_val] = 'outlier'
                df_base[col] = series
        # # # 找到所有值全为 0 的列
        # # zero_columns = (df_base == 0).all()
        #
        # print(df_base.dtypes)
        #
        # # 一个列表，用于记录被替换的列
        # replaced_columns = []
        #
        # # 记录成功转换的列
        # converted_columns = []
        #
        # # 遍历所有 object 类型的列
        # for col in df_base.select_dtypes(include='object').columns:
        #     try:
        #         # 尝试将列转换为数值（失败的变为 NaN）
        #         numeric_col = pd.to_numeric(df_base[col], errors='coerce')
        #
        #         # 如果转换后没有 NaN（说明是完全可转换的数值列）
        #         if numeric_col.notna().all():
        #             # 判断是整数还是浮点
        #             if (numeric_col == numeric_col.astype(int)).all():
        #                 df_base[col] = numeric_col.astype('int64')
        #             else:
        #                 df_base[col] = numeric_col.astype('float64')
        #             converted_columns.append(col)
        #     except Exception as e:
        #         print(f"列 {col} 转换失败：{e}")
        #
        # print(df_base.dtypes)

        # # 如果1到N 为空   但是N+1有数值   1到N就设为0
        # for col in cols:
        #     try:
        #         if df_base[df_base[col].isna()].index[0] == 0:
        #             idx = df_base[df_base[col].notna()].index[0]
        #             df_base[col].iloc[0:idx] = -1
        #             # print(col,idx)
        #     except:
        #         pass
        #
        # for col in cols:
        #     col_list = df_base[col].dropna().tolist()
        #     # 获得该列的上四分数*5的值
        #     max_val = np.percentile(col_list, 75) * 5
        #     series = df_base[col]
        #     # 将大于的值 填充为outlier
        #     series[series > max_val] = 'outlier'
        #     df_base[col] = series

        # 统计异常和缺失的数量  全部到新的表
        # 空值部分
        df_na = df_base.isna().sum().iloc[5:].to_frame().T.assign(type='NA')
        # 异常值部分
        df_outlier = (df_base == 'outlier').sum().iloc[5:].to_frame().T.assign(type='outlier')
        df_concat = pd.concat([df_na, df_outlier])
        df_concat.insert(0, 'file', filename)
        df_statistics = pd.concat([df_statistics, df_concat])

        # 将 outlier 替换 空值
        df_base = df_base.replace('outlier', np.nan)

        df_base = (
            df_base.astype(
                {
                    "Year": str,
                    "Month": str,
                    "Day": str,
                    "Hour": str,
                }
            )
            .assign(datetime=lambda x: x['Year'] + '-' + x['Month'] + '-' + x['Day'] + ' ' + x['Hour'].str.zfill(2))
            # .tail()
            .astype({'datetime': 'datetime64[ns]'})
            .set_index('datetime')
        )

        # 找到对应行的空值所在的时间
        for col in cols:
            df_col_na = df_base[df_base[col].isna()].loc[:, [col]]
            datetime_list = df_col_na.index.to_list()
            for datetime in datetime_list:

                # 偏移1小时
                try:
                    hour_start = datetime - pd.offsets.Hour(1)
                    hour_end = datetime + pd.offsets.Hour(1)
                    val_hour = (df_base.loc[hour_start, col] + df_base.loc[hour_end, col]) / 2
                except:
                    val_hour = np.nan

                # 偏移1天
                try:
                    day_start = datetime - pd.offsets.Day(1)
                    day_end = datetime + pd.offsets.Day(1)
                    # 偏移1天
                    val_day = (df_base.loc[day_start, col] + df_base.loc[day_end, col]) / 2
                except:
                    val_day = np.nan

                # 偏移一周
                try:
                    week_start = datetime - pd.offsets.Week(1)
                    week_end = datetime + pd.offsets.Week(1)
                    # 偏移一周
                    val_week = (df_base.loc[week_start, col] + df_base.loc[week_end, col]) / 2
                except:
                    val_week = np.nan

                # 偏移一月
                try:
                    month_start = datetime - pd.offsets.Day(30)
                    month_end = datetime + pd.offsets.Day(30)
                    # 偏移一月
                    val_month = (df_base.loc[month_start, col] + df_base.loc[month_end, col]) / 2
                except:
                    val_month = np.nan

                vals = (val_hour, val_day, val_week, val_month)

                try:
                    val = round(pd.Series(vals).dropna().iat[0], 3)
                    # print(val)
                except:
                    val = df_base[col].dropna().sample(1, random_state=77).iat[0]
                # 填充值
                df_base.loc[datetime, col] = val

        df_base = df_base.reset_index(drop=True)
        # df_base['Total Energy'] = df_base['Electricity']*3.41/1000 + df_base['Cooling']*3.41/0.284/1000 + df_base['Heat']
        df_base['Total Energy'] = (
                df_base['Electricity'].clip(lower=0) * 3.41 / 1000 +
                df_base['Cooling'].clip(lower=0) * 3.41 / 0.284 / 1000 +
                df_base['Heat'].clip(lower=0)
        )
        df_base['Total Energy'] = df_base['Total Energy'].round(2)
        # df_base['Emission'] = (df_base['Total Energy']*1000/3.41-df_base['PV'])/1000/2204.62*(1191.35+0.01913*21+0.01558*310)
        df_base['Emission'] = (
                (df_base['Total Energy'] * 1000 / 3.41 - df_base['PV'].clip(lower=0)) / 1000 / 2204.62 *
                (1191.35 + 0.01913 * 21 + 0.01558 * 310)
        )
        df_base['Emission'] = df_base['Emission'].round(2)
        # print(df_base.dtypes)
        # 只选择数值列用于判断
        numeric_cols = df_base.select_dtypes(include=[np.number]).columns

        # 找出所有数值列中所有值都接近0的列
        zero_columns = [
            col for col in numeric_cols
            if np.isclose(df_base[col], 0).all()
        ]

        # 替换这些列中的所有值为 -1
        for col in zero_columns:
            df_base[col] = -1
        df_base.to_csv(f'处理后的文件/{filename}.csv', index=False)
    df_statistics.to_csv('空值异常值统计.csv', index=False)


def run2():
    df_dict = {
        "CN01": [1, 11],
        "CN02": [12, 36],
        "CN03": [37, 136],
        "CN04": [137, 147],
    }

    for idx, lis in df_dict.items():
        df_res = pd.read_csv(f"处理后的文件\\BN001_energy.csv").set_index(
            ["Year", "Month", "Day", "Hour", "Weekday"]).applymap(lambda x: 0)
        start = lis[0]
        end = lis[1]
        for num in range(start, end + 1):
            num = str(num).zfill(3)
            filename = f'处理后的文件\\BN{num}_energy.csv'
            df = pd.read_csv(filename).set_index(["Year", "Month", "Day", "Hour", "Weekday"])
            # print(df.shape)

            try:
                df_res += df
            except:
                print(filename)
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
    df_res2.reset_index().to_csv(f'最终文件/Total.csv', index=False)


if __name__ == '__main__':
    shutil.rmtree('处理后的文件',ignore_errors=True)
    shutil.rmtree('最终文件',ignore_errors=True)
    os.makedirs('处理后的文件', exist_ok=True)
    os.makedirs('最终文件', exist_ok=True)
    run1()
    run2()