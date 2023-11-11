# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/13 14:40
# @Author : Hexk
# @Descript :
import os
import PathOperation.PathGetFiles as PGFiles
import RasterCalculate.RasterCalculator as RC

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231113_3_ERA5_RasterMergeMean'
    raster_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231113_4_ERA5_RasterMean'
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    for path_index, path_item in enumerate(raster_path_list):
        RC.RasterDivide(path_item, raster_output_folder, _denominator=12*23)


