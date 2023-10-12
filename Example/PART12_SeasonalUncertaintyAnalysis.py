# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/11 19:03
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
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231009\2_PredictData\4_MeanData'
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231008\1_PredictData\3_MaskData\Mask_NASA_2019_Bin_50\Reclassify\Reclassify.tif"
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231009\3_CSVData\4_UncertaintyCSV'
    IXGBR.ElevationUncertaintyAnalysis(raster_folder, reclassify_path, output_csv_folder)
