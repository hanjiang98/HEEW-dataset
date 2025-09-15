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
    base_files = glob.glob("raw data/*.csv")
    df_statistics = pd.DataFrame()
    for base_file in base_files:
        filename = base_file.split('\\')[-1].split('.')[0]
        # J 列不要
        df_base = pd.read_csv(base_file).drop(['Wind', 'Condition'], axis=1)

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
        df_base.to_csv(f'处理后的文件/{filename}.csv', index=False)


if __name__ == '__main__':
    shutil.rmtree('处理后的文件',ignore_errors=True)
    os.makedirs('处理后的文件', exist_ok=True)
    run1()