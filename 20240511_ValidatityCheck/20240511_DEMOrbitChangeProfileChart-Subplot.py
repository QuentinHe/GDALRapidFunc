# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/11 下午3:26
# @Author : Hexk
# @Descript : 其中含有高程剖面图，按道理说需要再给他几个细节或者多几条剖线。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import matplotlib.pyplot as plt

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_2_ProfilePointCSV\20240511_1_ProfilePoint.xlsx"
    excel_data = pd.read_excel(excel_path, sheet_name='20240511_1_ProfilePoint')
    srtm_dem_list = excel_data['SRTM_DEM']
    predict_dem_list = excel_data['Predict_DEM']
    icesat2_list = excel_data['H_Li']
    latitudes_list = excel_data['Latitudes']
    # x_list = [i for i in range(len(srtm_dem_list))]

    plt.rc('font', family='Times New Roman', size=14)
    plt.figure(dpi=300)
    plt.plot(latitudes_list, icesat2_list, linewidth=2, alpha=1, c='#008B8B', label='ICESat-2')
    plt.plot(latitudes_list, srtm_dem_list, linewidth=1.5, alpha=0.8, linestyle='solid', c='#FF8C00', label='SRTM DEM')
    plt.plot(latitudes_list, predict_dem_list, linewidth=1.5, alpha=0.8, linestyle='solid', c='#DC143C',
             label='Predict DEM')
    # plt.text(x=11, y=-3.5, s='A=1.2', ha='center', va='center',
    #          fontdict={'fontsize': 16, 'color': '#D32F2F'})
    # plt.xticks(ticks=month_labels)
    plt.xlabel('Latitudes (°)', fontsize=16)
    plt.ylabel('Glacier Elevation Change (m)', fontsize=16)
    plt.legend(prop={'size': 12})

    plt.tight_layout()
    plt.show()
