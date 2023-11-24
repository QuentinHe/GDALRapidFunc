# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/14 下午8:26
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

import PathOperation.PathGetFiles as PGF
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':

    # SRTM数据
    srtm_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions'
    srtm_path_list, srtm_name_list = PGF.PathGetFiles(srtm_folder, '.tif')

    """
    PART 2
    """
    xgboost_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\12_XGBoost_Data'
    # 融合
    bin_list = ['B50', 'B100', 'B150', 'B200']
    bin_num_list = ['50', '100', '150', '200']
    ctype_list_abb = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10']
    ctype_list = ['Minus5', 'Minus10', 'Plus5', 'Plus10', 'Random5', 'Random10']
    merge_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\13_Merge_Data'
    for bin_index, bin_item in enumerate(bin_list):
        for ctype_index, ctype_item in enumerate(ctype_list_abb):
            predict_folder = os.path.join(xgboost_output_folder, f'SRTM_{bin_item}_{ctype_item}')
            raster_reclassify_path = None
            print('正在寻找SRTM的相关DEM产品路径...')
            for dem_productions_index, dem_productions_item in enumerate(srtm_name_list):
                if f'Reclassify{bin_num_list[bin_index]}' in dem_productions_item and f'{ctype_list[ctype_index]}' in dem_productions_item:
                    print(f'已经找到{ctype_list[ctype_index]}的Reclassify{bin_num_list[bin_index]}文件.')
                    raster_reclassify_path = srtm_path_list[dem_productions_index]
            # print(raster_reclassify_path)
            IXGBR.MergeMultipleRegressionClassify(predict_folder, raster_reclassify_path, merge_output_folder, bins=bin_item, ctype= ctype_item)
