# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/14 下午10:30
# @Author : Hexk
# @Descript :
import os
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\15_Mean_Data'
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\14_Mask_Data"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\16_Year_Change_Data'
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\20_Year_Change_CSV'
    IXGBR.YearChangeMultipleAnalysis(raster_folder, reclassify_path, output_folder, output_csv_folder,
                                     _threshold=100)
