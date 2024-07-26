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
    # 轨道1
    # csv_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_2_ProfilePointCSV\20240511_1_ProfilePoint.xlsx"
    # csv_data = pd.read_excel(csv_path, sheet_name='20240511_1_ProfilePoint')
    # 轨道2 R轨道
    csv_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_2_ProfilePointCSV\20240512_1-R_ProfilePoint.xlsx"
    csv_data = pd.read_excel(csv_path, sheet_name='20240512_1-R_ProfilePoint')
    srtm_dem_list = csv_data['SRTM_DEM']
    predict_dem_list = csv_data['Predict_DEM']
    icesat2_list = csv_data['H_Li']
    latitudes_list = csv_data['Latitudes']
    # x_list = [i for i in range(len(srtm_dem_list))]

    plt.rc('font', family='Times New Roman', size=14)
    plt.figure(dpi=600)
    plt.plot(latitudes_list, icesat2_list, linewidth=2, alpha=0.6, c='#008B8B', label='ICESat-2')
    plt.plot(latitudes_list, srtm_dem_list, linewidth=1, alpha=0.8, linestyle='solid', c='#FF8C00', label='SRTM')
    plt.plot(latitudes_list, predict_dem_list, linewidth=0.8, linestyle='-.', c='#DC143C', label='Predict')
    # plt.text(x=11, y=-3.5, s='A=1.2', ha='center', va='center',
    #          fontdict={'fontsize': 16, 'color': '#D32F2F'})
    # plt.xticks(ticks=month_labels)
    plt.xlabel('Latitudes (°)', fontsize=16, fontweight='bold')
    plt.ylabel('Elevation (m)', fontsize=16, fontweight='bold')
    plt.yticks(rotation=90, va='center')

    # Part1
    # plt.text(33.1, 6100, 'ICESat-2 Track1', fontsize=20, fontweight='bold', fontstyle='italic', color='#604bc2')
    # plt.legend(prop={'size': 12})
    # Part2
    plt.text(33.15, 6400, 'ICESat-2 Track2', fontsize=20, fontweight='bold', fontstyle='italic', color='#43a1e2')
    plt.legend(prop={'size': 12}, loc=(0.5, 0.75))

    plt.tight_layout()
    # Part1
    # plt.savefig(r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Image\20240511_1_ProfilePoint.jpeg")
    # Part2
    plt.savefig(r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Image\20240512_1-R_ProfilePoint.jpeg")

    plt.show()
