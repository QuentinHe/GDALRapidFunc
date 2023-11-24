# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/11 上午9:51
# @Author : Hexk
# @Descript : 计算一下SRTM DEM和ICESat-2 Point测量值之间在每个Bin上的标准差。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    merge_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\1_PreTest_ICESat-2PointData\11_MergePoint\SRTM_Bin_50\SRTM_Bin_50.shp"
    original_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_BaseDEM\SRTM_DEM\SRTM_DEM.tif"
    point_rpdf = RSDF.ReadPoint2DataFrame(merge_point_path)
    point_df = point_rpdf.ReadShapeFile()
    # 统计每个bin level中有多少个点。
    bins_std = []
    for i in range(int(point_df['Bin_50'].min()), int(point_df['Bin_50'].max()) + 1):
        temp_df = point_df[point_df["Bin_50"] == float(i)]
        temp_df['temp_add'] = temp_df['Delta_Ele'] + temp_df['H_Li']
        print(temp_df['temp_add'].std())
