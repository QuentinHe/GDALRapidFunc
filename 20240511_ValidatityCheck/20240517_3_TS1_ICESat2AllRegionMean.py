# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/17 上午11:37
# @Author : Hexk
# @Descript :
import PathOperation.PathGetFiles as PGF
import PathOperation.PathFilesOperation as PFO
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR
import numpy as np
import ErrorAnalysis.ErrorAnalysis as EA
import os
import pandas as pd
import matplotlib.pyplot as plt

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    # 全区域实测值
    # point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\1_PreTest_ICESat-2PointData\11_MergePoint\SRTM_Bin_50\SRTM_Bin_50.shp"
    # 裁剪区域实测值
    point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_4_ClipPoint\20240515_SRTM_Point.shp"
    point_rsdf = RSDF.ReadPoint2DataFrame(point_path)
    point_df = point_rsdf.ReadShapeFile()
    #
    mean_list = []
    for i in range(int(min(point_df['Bin_50'])), int(max(point_df['Bin_50'])) + 1):
        temp_df = point_df[point_df['Bin_50'] == float(i)]
        mean_list.append(temp_df['Delta_Ele'].mean())
    print(mean_list)
    # print(point_df[point_df['Bin_50'] == 1.0]['Delta_Ele'].mean())
