# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/14 下午10:08
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR



if __name__ == '__main__':
    raster_folder = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\14_Mask_Data"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\15_Mean_Data'
    IXGBR.MeanBinsMultipleRaster(raster_folder, _output_path=output_folder)
