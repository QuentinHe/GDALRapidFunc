# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/12 下午3:05
# @Author : Hexk
# @Descript : 绘制他妈的散点图。纬度为横坐标，高程差为纵坐标。三年的icesat高程差是不同颜色。预测值是一种颜色。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    i2019_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_3_ContractOrbitPointShape\20240512_1_2019Point\20240512_1_2019Point.shp"
    i2020_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_3_ContractOrbitPointShape\20240512_2_2020Point\20240512_2_2020Point.shp"
    i2022_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240511_3_ContractOrbitPointShape\20240512_3_2022Point\20240512_3_2022Point.shp"

    i2019_rpdf = RPDF.ReadPoint2DataFrame(i2019_point_path)
    i2019_df = i2019_rpdf.ReadShapeFile()
    i2020_rpdf = RPDF.ReadPoint2DataFrame(i2020_point_path)
    i2020_df = i2020_rpdf.ReadShapeFile()
    i2022_rpdf = RPDF.ReadPoint2DataFrame(i2022_point_path)
    i2022_df = i2022_rpdf.ReadShapeFile()

    # 提取所有的纬度和行列号，以及predict dem值。
    predict_df = pd.DataFrame()
    i2019_temp_df = i2019_df[['Latitudes', 'Longitudes', 'Predict', 'H_SRTM', 'Row', 'Column']]
    i2020_temp_df = i2020_df[['Latitudes', 'Longitudes', 'Predict', 'H_SRTM', 'Row', 'Column']]
    i2022_temp_df = i2022_df[['Latitudes', 'Longitudes', 'Predict', 'H_SRTM', 'Row', 'Column']]
    predict_df = pd.concat([predict_df, i2019_temp_df, i2020_temp_df, i2022_temp_df])
    # predict_df删除Predict为0的行
    predict_df = predict_df.drop(predict_df[(predict_df['Predict']) == 0].index)
    # 去除行列重复的行
    predict_df = predict_df[predict_df.duplicated(subset=['Row', 'Column'], keep=False)]
    # i2019
    i2019_df = i2019_df.drop(i2019_df[(i2019_df['SRTM_DEM']) == 0].index)
    i2020_df = i2020_df.drop(i2020_df[(i2020_df['SRTM_DEM']) == 0].index)
    i2022_df = i2022_df.drop(i2022_df[(i2022_df['SRTM_DEM']) == 0].index)

    # 制图
    # 绘制散点图

    plt.rc('font', family='Times New Roman', size=14)
    plt.figure(dpi=300)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(predict_df['Latitudes'], predict_df['Longitudes'], predict_df['Predict'], s=15, color='none',
               edgecolors="#DC143C",
               marker='^',
               label='Predict')

    ax.scatter(i2019_df['Latitudes'], i2019_df['Longitudes'], i2019_df['H_SRTM'], s=10, marker='o', alpha=0.5,
               color='none',
               edgecolors="#fba834",
               label='ICESat-2 2019')
    ax.scatter(i2020_df['Latitudes'], i2020_df['Longitudes'], i2020_df['H_SRTM'], s=10, marker='o', alpha=0.5,
               color='none',
               edgecolors="#0779e4",
               label='ICESat-2 2020')
    ax.scatter(i2022_df['Latitudes'], i2022_df['Longitudes'], i2022_df['H_SRTM'], s=10, marker='o', alpha=0.5,
               color='none',
               edgecolors="#007944",
               label='ICESat-2 2022')
    ax.view_init(elev=22, azim=46)
    # plt.title(_title)
    ax.set_xlabel('Latitudes (°)', fontweight='bold')
    ax.set_ylabel('Longitudes (°)', fontweight='bold')
    ax.set_zlabel('Elevation Difference (m)', fontweight='bold')
    plt.legend(prop={'size': 14})
    plt.tight_layout()
    plt.show()
