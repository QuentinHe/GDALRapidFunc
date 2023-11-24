# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/25 14:43
# @Author : Hexk
# @Descript : 计算温度和降水的年平均变化率，2019-2018得到年变化量，之后22年的变化量求均值。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    # 这是12个月之和的数据，未除以12
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_2_WorldClimProcessResult\20231113_1_WCPR_MonthSum'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_2_WorldClimProcessResult\20231125_1_WCPR_YearSumReduceMean'
    raster_path_list, raster_path_name = PGFiles.PathGetFiles(raster_folder, '.tif')
    prec_path_list, prec_name_list, tmax_path_list, tmin_path_list, tmax_name_list, tmin_name_list = [], [], [], [], [], []
    for index, item in enumerate(raster_path_name):
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
    years_list = [i for i in range(2001, 2022)]
    sign_list = ['prec', 'tmax', 'tmin']
    for sign in sign_list:
        for year in years_list:
            after_path, before_path = None, None
            if sign == 'prec':
                for index, item in enumerate(prec_name_list):
                    if f'{sign}_{year}' == item:
                        after_path = prec_path_list[index]
                    if f'{sign}_{year - 1}' == item:
                        before_path = prec_path_list[index]
            elif sign == 'tmax':
                for index, item in enumerate(tmax_name_list):
                    if f'{sign}_{year}' == item:
                        after_path = tmax_path_list[index]
                    if f'{sign}_{year - 1}' == item:
                        before_path = tmax_path_list[index]
            else:
                for index, item in enumerate(tmin_name_list):
                    if f'{sign}_{year}' == item:
                        after_path = tmin_path_list[index]
                    if f'{sign}_{year - 1}' == item:
                        before_path = tmin_path_list[index]
            after_rr = RR.ReadRaster(after_path)
            before_rr = RR.ReadRaster(before_path)
            after_data = after_rr.ReadRasterFile()
            before_data = before_rr.ReadRasterFile()
            result_data = (after_data - before_data) / 12
            output_path = os.path.join(output_folder, f'{sign}_{year}-{year - 1}.tif')
            after_rr.WriteRasterFile(result_data, output_path, _nodata=0)

