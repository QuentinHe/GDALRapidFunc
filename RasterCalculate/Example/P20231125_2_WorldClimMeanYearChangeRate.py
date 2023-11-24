# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/25 15:16
# @Author : Hexk
# @Descript : 计算平均变化率
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
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_2_WorldClimProcessResult\20231125_1_WCPR_YearSumReduceMean'
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_2_WorldClimProcessResult\20231125_2_WCPR_YearMean'
    prec_path_list, prec_name_list, tmax_path_list, tmin_path_list, tmax_name_list, tmin_name_list = [], [], [], [], [], []
    for index, item in enumerate(raster_name_list):
        sign = item.split('_')[0]
        if sign == 'prec':
            prec_path_list.append(raster_path_list[index])
            prec_name_list.append(item)
        elif sign == 'tmax':
            tmax_path_list.append(raster_path_list[index])
            tmax_name_list.append(item)
        else:
            tmin_path_list.append(raster_path_list[index])
            tmin_name_list.append(item)
    RC.RasterAdd(prec_path_list[0], output_folder, *tuple(prec_path_list[1:]), _output_name='prec_Sum')
    RC.RasterAdd(tmax_path_list[0], output_folder, *tuple(tmax_path_list[1:]), _output_name='tmax_Sum')
    RC.RasterAdd(tmin_path_list[0], output_folder, *tuple(tmin_path_list[1:]), _output_name='tmin_Sum')
