# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/17 11:08
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
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\4_MeanData'
    # nasa_reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\3_MaskData\Mask_NASA_Bin_50_Month1\Reclassify\Reclassify.tif"
    srtm_reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\3_MaskData\Mask_SRTM_Bin_50_Month1\Reclassify\Reclassify.tif"
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\3_CSV\2_Intra\5_UncertaintyCSV'
    IXGBR.ElevationUncertaintyAnalysis(raster_folder, srtm_reclassify_path, output_csv_folder)
