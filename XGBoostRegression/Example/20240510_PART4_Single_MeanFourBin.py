# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/10 下午9:48
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR



if __name__ == '__main__':
    raster_folder = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\3_MaskData"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\4_MeanData'
    IXGBR.MeanBinsRaster(raster_folder, _output_path=output_folder)
