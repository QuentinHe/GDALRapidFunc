# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/13 14:47
# @Author : Hexk
# @Descript :
import os
import RasterCalculate.RasterCalculator as RC

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231113_4_ERA5_RasterMean\Divide_t2m_Sum.tif"
    raster_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231113_4_ERA5_RasterMean'
    RC.RasterReduce(raster_path, raster_output_folder, _reduced_num=273.15)
