# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/17 9:30
# @Author : Hexk
# @Descript :
import os
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import PathOperation.PathGetFiles as PGF
import ReadRasterAndShape.ReadRaster as RR
import numpy as np
import pandas as pd
import time

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\4_MeanData'
    nasa_reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\3_MaskData\Mask_NASA_Bin_50_Month1\Reclassify\Reclassify.tif"
    srtm_reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\3_MaskData\Mask_SRTM_Bin_50_Month1\Reclassify\Reclassify.tif"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\5_SeasonalChangeData'
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\3_CSV\2_Intra\4_SeasonalChangeCSV'
    raster_path_list, raster_file_list = PGF.PathGetFiles(raster_folder, '.tif')
    nasa_list = []
    srtm_list = []
    for index, item in enumerate(raster_file_list):
        if 'NASA' in item:
            nasa_list.append(raster_path_list[index])
        else:
            srtm_list.append(raster_path_list[index])
    print(nasa_list)
    print(srtm_list)
    IXGBR.SeasonalChangeAnalysis(nasa_list, nasa_reclassify_path, output_csv_folder, 'NASA_Month', _threshold=100)
    IXGBR.SeasonalChangeAnalysis(srtm_list, srtm_reclassify_path, output_csv_folder, 'SRTM_Month', _threshold=100)
