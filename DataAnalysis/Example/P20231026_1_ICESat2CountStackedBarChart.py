# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/26 9:49
# @Author : Hexk
# @Descript : ICESat2年月数据点图：堆叠柱状图和折线图
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import matplotlib.pyplot as plt

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\2_Method&Data\1_Landsat.xlsx"
df = pd.read_excel(excel_path, sheet_name=1)
months_labels = df.columns[1:]
year_2019_num = df.iloc[0, 1:]
year_2020_num = df.iloc[1, 1:]
year_2021_num = df.iloc[2, 1:]
year_2022_num = df.iloc[3, 1:]
nums_sum = year_2019_num + year_2020_num + year_2021_num + year_2022_num

plt.rc('font', family='Times New Roman', size=14)
# 绘制堆叠柱状图
# plt.figure(dpi=300)
width = 0.4
p1 = plt.bar(months_labels, year_2019_num, width, label='ICESat2 2019', color='#22668d', ec='grey', lw=0.2)
p2 = plt.bar(months_labels, year_2020_num, width, bottom=year_2019_num, label='ICESat2 2020', color='#8ecddd',
             ec='grey',
             lw=0.2)
p3 = plt.bar(months_labels, year_2021_num, width, bottom=(year_2020_num + year_2019_num), label='ICESat2 2021',
             color='#fffadd', ec='grey', lw=0.2)
p4 = plt.bar(months_labels, year_2022_num, width, bottom=(year_2021_num + year_2020_num + year_2019_num),
             label='ICESat2 2022',
             color='#ffcc70', ec='grey', lw=0.2)
plt.xticks(range(1, 13))
plt.yticks([i * 5000 for i in range(1, 7)], labels=[f'{i * 5}k' for i in range(1, 7)])
plt.xlabel('Month', fontsize=16)
plt.ylabel('Numbers of ICESat2 Footprints', fontsize=16)
plt.legend(frameon=False, prop={'size': 12})
plt.tight_layout()
# 绘制折线图
plt.plot(months_labels, nums_sum, '-.o', c='#e55604', lw=1, markersize=5)
for x, y in zip(months_labels, nums_sum):
    plt.text(x, y, f'{np.around(y / 1000, decimals=1)}k', ha='center', va='bottom', c='#3d0c11')
plt.savefig(
    r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\2_Method&Data\20231026_1_ICESat2PointCount.png')
plt.tight_layout()
plt.show()
