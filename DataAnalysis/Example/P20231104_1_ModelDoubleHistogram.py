# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/4 14:41
# @Author : Hexk
# @Descript : 绘制双柱状直方图，共用一个X轴，双Y轴，同时用透明斜线填充表示。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import matplotlib.pyplot as plt
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    csv_path_1 = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\YearValidationResultCSV.csv"
    csv_path_2 = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\SeasonalValidationResultCSV.csv"
    year_csv_df = pd.read_csv(csv_path_1)
    seasonal_csv_df = pd.read_csv(csv_path_2)
    year_r2 = year_csv_df['R2']
    year_rmse = year_csv_df['RMSE']
    seasonal_r2 = seasonal_csv_df['R2']
    seasonal_rmse = seasonal_csv_df['RMSE']

    plt.rc('font', family='Times New Roman', size=12)
    plt.figure(figsize=(8, 6))
    # 绘制第一个子图 年变化拟合的R2
    plt.subplot(221)
    plt.hist(year_r2, color='#82aae3', ec='#1a374d', label='Annual changes')
    plt.xlabel('Correlation Coefficient')
    plt.ylabel('Number of elevation bins')
    plt.legend()
    # 绘制第二个子图 年变化拟合的RMSE
    plt.subplot(222)
    plt.hist(year_rmse, color='#82aae3', ec='#1a374d', label='Annual changes')
    plt.xlabel('RMSE (m)')
    plt.ylabel('Number of elevation bins')
    plt.legend()
    # 绘制第三个子图 月变化拟合的R2
    plt.subplot(223)
    plt.hist(seasonal_r2, color='#ece3ce', ec='#1a374d', label='Monthly changes')
    plt.xlabel('Correlation Coefficient')
    plt.ylabel('Number of elevation bins')
    plt.legend()
    # 绘制第四个子图 月变化拟合的RMSE
    plt.subplot(224)
    plt.hist(seasonal_rmse, color='#ece3ce', ec='#1a374d', label='Monthly changes')
    plt.xlabel('RMSE (m)')
    plt.ylabel('Number of elevation bins')
    plt.tight_layout()
    plt.legend()
    plt.show()
