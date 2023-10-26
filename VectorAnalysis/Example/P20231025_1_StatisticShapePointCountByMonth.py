# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/25 21:31
# @Author : Hexk
# @Descript : 统计每个月有多少个点，输出成csv
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import VectorAnalysis.ShapePointCountStatistic as SPCS
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    shape_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\7_Remove_Slope_Data'
    shape_path_list, shape_name_list = PGFiles.PathGetFiles(shape_folder, '.shp')
    srtm_path_list, srtm_name_list = [], []
    for index, item in enumerate(shape_name_list):
        if 'SRTM' in item:
            srtm_name_list.append(item)
            srtm_path_list.append(shape_path_list[index])
    # 统计每个月有多少个点
    for index, item in enumerate(srtm_path_list):
        output_name = f'{srtm_name_list[index]}_MonthCount.csv'
        output_path = os.path.join(shape_folder, output_name)
        SPCS.ShapeCountStatisticByDate(item, ['Date'], _output_csv_path=output_path)


