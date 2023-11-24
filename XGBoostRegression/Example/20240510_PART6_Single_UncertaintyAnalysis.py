# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/10 下午9:57
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

import XGBoostRegression.IntegrationXGBoostRegression as IXGBR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\4_MeanData'
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\3_MaskData\Mask_SRTM_2019_Bin_50\Mask_SRTM_2019_Bin_50\Reclassify\Reclassify.tif"
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\3_PreTest_CSV\5_UncertaintyCSV'
    # 这里需要根据icesat-2 point 重写误差值判定公式。
    merge_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\1_PreTest_ICESat-2PointData\11_MergePoint\SRTM_Bin_50\SRTM_Bin_50.shp"
    IXGBR.ElevationUncertaintyAnalysisNewFormula(raster_folder, reclassify_path, merge_point_path, output_csv_folder)
