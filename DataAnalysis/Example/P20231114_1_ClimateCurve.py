# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/14 10:17
# @Author : Hexk
# @Descript : 绘制年 月变化的温度和降水曲线，同时绘制出趋势线
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_2_WorldClimProcessResult\20231113_4_WCPR_Excel\WorldClim_Result.xlsx"
    t_year_df = pd.read_excel(excel_path, sheet_name='tmax_Year')
    t_month_df = pd.read_excel(excel_path, sheet_name='tmax_Month')
    prec_year_df = pd.read_excel(excel_path, sheet_name='prec_Year')
    prec_month_df = pd.read_excel(excel_path, sheet_name='prec_Month')

    # plt.style.use('ggplot')
    plt.rc('font', family='Times New Roman', size=22)

    plt.figure(figsize=(8, 16), dpi=300)
    p1 = plt.subplot(311)
    t_year_label = t_year_df['Year']
    t_year_data = t_year_df['T_Mean']
    p1.plot(t_year_label, t_year_data, c='#f39233', marker='o', markersize=4, markeredgewidth=1)
    p1.set_xlabel('Year', fontdict={"size": 26})
    p1.set_ylabel('Average Temperature (℃)', fontdict={"size": 26})
    p1_slope, p1_intercept = np.polyfit(t_year_label, t_year_data, 1)
    p1_line = p1_slope * t_year_label + p1_intercept
    p1.plot(t_year_label, p1_line, color='#2d6187', linestyle='--', linewidth=2)

    p2 = plt.subplot(312)
    prec_year_label = prec_year_df['Year']
    prec_year_data = prec_year_df['prec_Mean']
    p2.bar(prec_year_label, prec_year_data, fc='#adc4ce')
    p2.plot(prec_year_label, prec_year_data, c='#3876bf', marker='s', markersize=4, markeredgewidth=1)
    p2.set_xlabel('Year', fontdict={"size": 26})
    p2.set_ylabel('Average Precipitation (mm)', fontdict={"size": 26})
    p2_slope, p2_intercept = np.polyfit(prec_year_label, prec_year_data, 1)
    p2_line = p2_slope * prec_year_label + p2_intercept
    p2.plot(prec_year_label, p2_line, color='#f39233', linestyle='--', linewidth=2)

    ax1 = plt.subplot(313)
    month_label = t_month_df['Month']
    t_month_data = t_month_df['T_Mean']
    prec_month_data = prec_month_df['prec_Mean']
    ax1.bar(month_label, prec_month_data, fc='#3876bf', label='PRCP')
    ax1.set_ylabel('Average Precipitation (mm)', fontdict={"size": 26})
    ax1.set_xlabel('Month', fontdict={"size": 26})
    ax2 = ax1.twinx()
    ax2.plot(month_label, t_month_data, c='#f39233', marker='^', markersize=4, markeredgewidth=1, label='TEMP')
    ax2.set_ylabel('Average Temperature (℃)')
    ax1.legend(loc='upper left', frameon=False)
    ax2.legend(loc='upper right', frameon=False)

    plt.tight_layout()
    plt.savefig(
        r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\20231207_8_Figure12.jpeg')
    plt.show()
