# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/22 10:37
# @Author : Hexk
# @Descript : 合并ERA5的风速数据
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
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231122_1_ERA5Wind\20231122_1_WindTif'
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    si10_path_list, si10_name_list, u10_path_list, u10_name_list, v10_path_list, v10_name_list = [], [], [], [], [], []
    for index, item in enumerate(raster_name_list):
        name = os.path.splitext(item)[0].rsplit('_', 1)[1]
        if 'si10' == name:
            si10_name_list.append(item)
            si10_path_list.append(raster_path_list[index])
        elif 'u10' == name:
            u10_name_list.append(item)
            u10_path_list.append(raster_path_list[index])
        else:
            v10_name_list.append(item)
            v10_path_list.append(raster_path_list[index])
    si10_path_tuple = tuple(si10_path_list)
    si10_name_tuple = tuple(si10_name_list)
    u10_path_tuple = tuple(u10_path_list)
    u10_name_tuple = tuple(u10_name_list)
    v10_path_tuple = tuple(v10_path_list)
    v10_name_tuple = tuple(v10_name_list)
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231122_1_ERA5Wind\20231122_2_WindTifAdd'
    RC.RasterAdd(si10_path_tuple[0], output_folder, *si10_path_tuple[1:], _output_name='20231122_2_WindTifAdd_si10')
    RC.RasterAdd(u10_path_tuple[0], output_folder, *u10_path_tuple[1:], _output_name='20231122_2_WindTifAdd_u10')
    RC.RasterAdd(v10_path_tuple[0], output_folder, *v10_path_tuple[1:], _output_name='20231122_2_WindTifAdd_v10')
