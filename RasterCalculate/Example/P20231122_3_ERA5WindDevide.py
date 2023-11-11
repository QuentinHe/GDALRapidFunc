# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/22 10:51
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
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231122_1_ERA5Wind\20231122_2_WindTifAdd'
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder,'.tif')
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231122_1_ERA5Wind\20231122_3_WindTifDevide'
    raster_path_tuple = tuple(raster_path_list)
    RC.RasterDivide(raster_path_tuple[0], output_folder, *raster_path_tuple[1:], _denominator=23*12)