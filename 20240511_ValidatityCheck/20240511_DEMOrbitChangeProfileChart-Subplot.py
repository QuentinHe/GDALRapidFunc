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
    # excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_2_ProfilePointCSV\20240511_1_ProfilePoint.xlsx"
    # 轨道2 R轨道
    excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_2_ProfilePointCSV\20240512_1-R_ProfilePoint.xlsx"
    excel_data = pd.read_excel(excel_path, sheet_name='Part1')

    srtm_dem_list = excel_data['SRTM_DEM']
    predict_dem_list = excel_data['Predict_DEM']
    icesat2_list = excel_data['H_Li']
    latitudes_list = excel_data['Latitudes']
    # x_list = [i for i in range(len(srtm_dem_list))]

    plt.rc('font', family='Times New Roman', size=24)
    plt.figure(dpi=300)

    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内

    plt.plot(latitudes_list, icesat2_list, linewidth=3, alpha=1, c='#008B8B', label='ICESat-2')
    plt.plot(latitudes_list, srtm_dem_list, linewidth=2, alpha=0.8, linestyle='solid', c='#FF8C00', label='SRTM')
    plt.plot(latitudes_list, predict_dem_list, linewidth=2, alpha=0.8, linestyle='solid', c='#DC143C',
             label='Predict')
    # plt.text(x=11, y=-3.5, s='A=1.2', ha='center', va='center',
    #          fontdict={'fontsize': 16, 'color': '#D32F2F'})
    plt.yticks(rotation=90, va='center')
    # Part1
    # plt.xticks(np.linspace(33.25, 33.33, 5))
    # Part2
    # PART3
    # plt.xticks(np.linspace(33.55, 33.58, 4))
    # plt.xlabel('Latitudes (°)', fontsize=16)
    # plt.ylabel('Glacier Elevation Change (m)', fontsize=16)
    plt.xticks([])
    plt.legend(prop={'size': 24})

    plt.tight_layout()
    # Track1 Part1
    # plt.savefig(r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Image\20240511_1_ProfilePoint-Part1-Big.jpeg")
    # Track1 Part2
    # plt.savefig(r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Image\20240511_1_ProfilePoint-Part2-Big.jpeg")
    # Track1 Part3
    # plt.savefig(r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Image\20240511_1_ProfilePoint-Part3-Big.jpeg")
    # Track2 Part1
    plt.savefig(r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Image\20240512_1-R_ProfilePoint-Part1-Big.jpeg")
    # Track2 Part2
    # plt.savefig(r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Image\20240512_1-R_ProfilePoint-Part2-Big.jpeg")
    plt.show()