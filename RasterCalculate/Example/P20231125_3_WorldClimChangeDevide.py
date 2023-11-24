# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/25 15:23
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles
import ReadRasterAndShape.ReadRaster as RR
import RasterCalculate.RasterCalculator as RC

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_2_WorldClimProcessResult\20231125_2_WCPR_YearMean'
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_2_WorldClimProcessResult\20231125_3_WCPR_Devide'
    RC.RasterDivide(raster_path_list[0], output_folder, *tuple(raster_path_list[1:]), _denominator=21)
