# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/7 14:41
# @Author : Hexk
# @Descript : 统计冰川整体冰川的年变化情况

import os
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\4_MeanData'
    # reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\3_MaskData\Mask_NASA_2019_Bin_50\Reclassify\Reclassify.tif"
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\3_MaskData\Mask_SRTM_2019_Bin_50\Reclassify\Reclassify.tif"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\5_YearChangeData'
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\3_CSV\1_Inter\4_YearChangeCSV'
    IXGBR.YearChangeAnalysis(raster_folder, reclassify_path, output_folder, output_csv_folder,
                             _threshold=100,
                             _mode='divide')
