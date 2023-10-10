# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/7 11:23
# @Author : Hexk
# @Descript : 对每年的4个Bin等级对应点进行平均
import os
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231008\1_PredictData\3_MaskData'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231008\1_PredictData\4_MeanData\20231009_1'
    IXGBR.MeanBinsRaster(raster_folder, _output_path=output_folder)
