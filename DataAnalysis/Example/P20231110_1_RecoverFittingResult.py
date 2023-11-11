# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/10 16:28
# @Author : Hexk
# @Descript : 20231110_4_RecoverFitting
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import matplotlib.pyplot as plt

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\Result_WholeGlaicerMonthlyChange.xlsm"
    result_df = pd.read_excel(excel_path, sheet_name='Result')
    month_labels = [i for i in range(1, 13)]
    plt.rc('font', family='Times New Roman', size=14)
    plt.plot(month_labels, list(result_df.iloc[0])[1:], c='#1976D2', marker='o', markersize=5, markeredgewidth=1.5,
             label=result_df['Name'][0])
    plt.plot(month_labels, list(result_df.iloc[1])[1:], c='#00796B', marker='^', markersize=5, markeredgewidth=1.5,
             label=result_df['Name'][1])
    plt.plot(month_labels, list(result_df.iloc[2])[1:], c='#FF6D00', marker='s', markersize=5, markeredgewidth=1.5,
             label=result_df['Name'][2])
    plt.text(x=11, y=-3.5, s='A=1.2', ha='center', va='center',
             fontdict={'fontsize': 16, 'color': '#D32F2F'})
    plt.xticks(ticks=month_labels)
    plt.xlabel('Month', fontsize=16)
    plt.ylabel('Glacier Elevation Change(m)', fontsize=16)
    plt.legend(prop={'size': 12})
    plt.tight_layout()
    plt.show()
