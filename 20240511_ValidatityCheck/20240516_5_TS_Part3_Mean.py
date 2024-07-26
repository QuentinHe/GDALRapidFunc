# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/16 下午3:31
# @Author : Hexk
# @Descript :

import shutil
import PathOperation.PathGetFiles as PGF
import PathOperation.PathFilesOperation as PFO
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR
import numpy as np
import ErrorAnalysis.ErrorAnalysis as EA
import os
import pandas as pd

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    # RGI区域
    rgi_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\1_GlaciersRegion\1_GlaciersRegion.shp"
    # 基准DEM
    dem_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\4_BaseSRTMDEM'
    dem_path_list, dem_files_list = PGF.PathGetFiles(dem_folder, '.tif')
    # SRTM数据
    srtm_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\5_BaseDEMProductions\SRTM'
    srtm_path_list, srtm_files_list = PGF.PathGetFiles(srtm_folder, '.tif')
    # 公共数据
    # 公共数据只有projx projy
    common_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\CommonData'
    common_path_list, common_files_list = PGF.PathGetFiles(common_folder, '.tif')
    # Point数据
    point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\7_TS_PointMerge\7_TS_PointMerge.shp"

    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\13_Mean'
    target_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\9_TS_MergeData_R10'
    raster_path_list, raster_name_list, = PGF.PathGetFiles(target_folder, '.tif')
    temple_rr = RR.ReadRaster(raster_path_list[0])
    temple_data = temple_rr.ReadRasterFile()
    temp_data = np.zeros(temple_data.shape)
    for raster_name_index, raster_name_item in enumerate(raster_name_list):
        raster_rr = RR.ReadRaster(raster_path_list[raster_name_index])
        raster_data = raster_rr.ReadRasterFile()
        temp_data += raster_data
    temp_data = temp_data/4
    output_path = os.path.join(output_folder, 'R10.tif')
    temple_rr.WriteRasterFile(temp_data, output_path)



