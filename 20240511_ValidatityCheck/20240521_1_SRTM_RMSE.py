# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/21 下午2:46
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import ErrorAnalysis.ErrorAnalysis as EA

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
# 计算SRTM DEM的RMSE
if __name__ == '__main__':
    # dem_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\4_BaseSRTMDEM\SRTM\SRTM_DEM.tif'
    dem_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\4_MeanData\SRTM_2019\SRTM_2019.tif'
    point_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\1_PreTest_ICESat-2PointData\11_MergePoint\SRTM_Bin_50\SRTM_Bin_50.shp'
    dem_rr = RR.ReadRaster(dem_path)
    dem_data = dem_rr.ReadRasterFile()
    point_rpdf = RPDF.ReadPoint2DataFrame(point_path)
    point_df = point_rpdf.ReadShapeFile()
    point_row, point_column = point_rpdf.PointMatchRasterRowColumn(dem_rr.raster_ds_geotrans)
    point_value_list = RR.SearchRasterRowColumnData(point_row, point_column, dem_data)
    point_df['SRTM_DEM'] = point_value_list
    rmse_list = []
    for i in range(1, 17):
        iceset_list = point_df[point_df['Bin_50'] == float(i)]['Delta_Ele']
        srtm_list = point_df[point_df['Bin_50'] == float(i)]['SRTM_DEM']
        rmse_list.append(EA.rmse(iceset_list, srtm_list))
    print(np.mean(rmse_list))

