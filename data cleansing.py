# -*- coding: utf-8 -*-
"""
# @Time    : 2023/10/3 
# @Author  : Hanjiang Dong
# @Intro   : Hi Larissa!
"""
import numpy as np
import pandas as pd

names = [
    ['Total'],
    ['CN01',
     'BN001', 'BN002', 'BN003', 'BN004', 'BN005', 'BN006', 'BN007', 'BN008', 'BN009', 'BN010',
     'BN011',
     ],
    ['CN02',
     'BN012', 'BN013', 'BN014', 'BN015', 'BN016', 'BN017', 'BN018', 'BN019', 'BN020',
     'BN021', 'BN022', 'BN023', 'BN024', 'BN025', 'BN026', 'BN027', 'BN028', 'BN029', 'BN030',
     'BN031', 'BN032', 'BN033', 'BN034', 'BN035', 'BN036',
     ],
    ['CN03',
     'BN037', 'BN038', 'BN039', 'BN040',
     'BN041', 'BN042', 'BN043', 'BN044', 'BN045', 'BN046', 'BN047', 'BN048', 'BN049', 'BN050',
     'BN051', 'BN052', 'BN053', 'BN054', 'BN055', 'BN056', 'BN057', 'BN058', 'BN059', 'BN060',
     'BN061', 'BN062', 'BN063', 'BN064', 'BN065', 'BN066', 'BN067', 'BN068', 'BN069', 'BN070',
     'BN071', 'BN072', 'BN073', 'BN074', 'BN075', 'BN076', 'BN077', 'BN078', 'BN079', 'BN080',
     'BN081', 'BN082', 'BN083', 'BN084', 'BN085', 'BN086', 'BN087', 'BN088', 'BN089', 'BN090',
     'BN091', 'BN092', 'BN093', 'BN094', 'BN095', 'BN096', 'BN097', 'BN098', 'BN099', 'BN100',
     'BN101', 'BN102', 'BN103', 'BN104', 'BN105', 'BN106', 'BN107', 'BN108', 'BN109', 'BN110',
     'BN111', 'BN112', 'BN113', 'BN114', 'BN115', 'BN116', 'BN117', 'BN118', 'BN119', 'BN120',
     'BN121', 'BN122', 'BN123', 'BN124', 'BN125', 'BN126', 'BN127', 'BN128', 'BN129', 'BN130',
     'BN131', 'BN132', 'BN133', 'BN134', 'BN135', 'BN136',
     ],
    ['CN04',
     'BN137', 'BN138', 'BN139', 'BN140',
     'BN141', 'BN142', 'BN143', 'BN144', 'BN145', 'BN146', 'BN147',
     ],
]

upperbound = [
    [9.30E+12, 0, 0, 22899.94]
]

for i in range(len(names)):
    for j in range(len(names[i])):
        print("************loading dataset/{str}_energy.csv".format(str=names[i][j]))
        df = pd.read_csv('dataset/{str}_energy.csv'.format(str=names[i][j]))

        # print("the number of -0.01 is {num}".format(num=(df == -0.01).sum().sum()))
        df.replace(-0.01, np.nan, inplace=True)

        # for name in list(df.columns)[5:-2]:
            # print("maximum of {str} is {num}".format(str=name, num=np.max(df[name])))
            # print("minimum of {str} is {num}".format(str=name, num=np.min(df[name])))
        df['Electricity'] = df['Electricity'].where((df['Electricity'] >= 0.0) & (df['Electricity'] <= 9.30E+12), np.nan)
        Electricity = (df['Electricity'] >= 0.0) & (df['Electricity'] <= 9.30E+12)
        df['PV'] = df['PV'].where((df['PV'] >= 0.0), np.nan)
        PV = (df['PV'] >= 0.0)
        df['Cooling'] = df['Cooling'].where((df['Cooling'] >= 0.0), np.nan)
        Cooling = (df['Cooling'] >= 0.0)
        df['Heat'] = df['Heat'].where((df['Heat'] >= 0.0) & (df['Heat'] <= 22899.94), np.nan)
        Heat = (df['Heat'] >= 0.0) & (df['Heat'] <= 22899.94)

        df['Total Energy'] = df['Total Energy'].where(Electricity, np.nan)
        df['Total Energy'] = df['Total Energy'].where(PV, np.nan)
        df['Total Energy'] = df['Total Energy'].where(Cooling, np.nan)
        df['Total Energy'] = df['Total Energy'].where(Heat, np.nan)
        df['Emission'] = df['Emission'].where(Electricity, np.nan)
        df['Emission'] = df['Emission'].where(PV, np.nan)
        df['Emission'] = df['Emission'].where(Cooling, np.nan)
        df['Emission'] = df['Emission'].where(Heat, np.nan)

        df.to_csv('{str}_energy.csv'.format(str=names[i][j]), index=False)
