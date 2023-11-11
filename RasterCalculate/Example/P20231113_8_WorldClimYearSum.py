# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/13 19:48
# @Author : Hexk
# @Descript :
import os
import PathOperation.PathGetFiles as PGFiles
import RasterCalculate.RasterCalculator as RC

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_2_WorldClimProcessResult\20231113_1_WCPR_MonthSum'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_2_WorldClimProcessResult\20231113_2_WCPR_YearSum'
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    type_list = ['prec', 'tmax', 'tmin']
    year_list = [i for i in range(2000, 2022)]
    for type_index, type_item in enumerate(type_list):
        # for year_index, year_item in enumerate(year_list):
        temp_raster_tuple = list(zip(range(len(raster_path_list)), raster_path_list))
        temp_filter_raster_tuple = list(filter(lambda x: str(type_item) in x[1], temp_raster_tuple))
        temp_result_list = list(list(zip(*temp_filter_raster_tuple))[1])
        RC.RasterAdd(temp_result_list[0], output_folder, *temp_result_list[1:], _output_name=f'{type_item}_Sum')
