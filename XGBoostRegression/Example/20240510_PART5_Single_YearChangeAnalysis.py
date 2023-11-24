# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/10 下午9:52
# @Author : Hexk
# @Descript :
import os
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\4_MeanData'
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\3_MaskData\Mask_SRTM_2019_Bin_50\Mask_SRTM_2019_Bin_50\Reclassify\Reclassify.tif"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\5_YearChangeData'
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\3_PreTest_CSV\4_YearChangeCSV'
    IXGBR.YearChangeAnalysis(raster_folder, reclassify_path, output_folder, output_csv_folder,
                             _threshold=100,
                             _mode='divide')
