# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/16 下午4:18
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
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\13_Mean'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\14_Mask'
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\15_OutputCSV'
    region_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\1_GlaciersRegion\1_GlaciersRegion.shp"
    reclassify_path =r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\5_BaseDEMProductions\SRTM\SRTM_Reclassify\SRTM_Reclassify_50\SRTM_Reclassify_50.tif"

    raster_path_list, raster_name_list, = PGF.PathGetFiles(raster_folder, '.tif')
    for index, item in enumerate(raster_name_list):
        output_mask_filepath = os.path.join(output_folder, f'Mask_{item}.tif')
        IXGBR.MaskRegionAnalysis(region_path, raster_path_list[index], output_mask_filepath, reclassify_path,
                                 _dem_type='SRTM',
                                 _bin_level='Bin_50', _year=2020,
                                 _output_csv_folder=output_csv_folder)
