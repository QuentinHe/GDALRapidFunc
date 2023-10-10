# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/8 15:03
# @Author : Hexk
# @Descript : 需要统计冰川整体的高程不确定性，分箱高程差的标准差，3倍标准差范围，3倍标准差过滤后值的高程变化量
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231008\1_PredictData\4_MeanData\20231009_1'
    # raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\1_PredictData\6_20231008\TEST'
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231008\1_PredictData\3_MaskData\Mask_NASA_2019_Bin_50\Reclassify\Reclassify.tif"
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231008\2_CSVData\4_UncertaintyCSV'
    IXGBR.ElevationUncertaintyAnalysis(raster_folder, reclassify_path, output_csv_folder)
