# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/16 下午2:42
# @Author : Hexk
# @Descript :
import PathOperation.PathGetFiles as PGF
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':

    # SRTM数据
    srtm_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\5_BaseDEMProductions\SRTM'
    srtm_path_list, srtm_files_list = PGF.PathGetFiles(srtm_folder, '.tif')

    """
    PART 2
    """
    xgboost_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\8_TS_XGBoostData_R10'
    # 融合
    dem_type_list = ['SRTM']
    bin_list = [i * 50 for i in range(1, 5)]
    merge_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\9_TS_MergeData_R10'
    for dem_index, dem_item in enumerate(dem_type_list):
        for bin_index, bin_item in enumerate(bin_list):
            predict_folder = os.path.join(xgboost_output_folder, f'{dem_item}_Bin_{bin_item}')
            raster_reclassify_path = None
            if dem_item == 'SRTM':
                print('正在寻找SRTM的相关DEM产品路径...')
                for dem_productions_index, dem_productions_item in enumerate(srtm_files_list):
                    if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
                        print(f'已经找到{dem_item}的Reclassify文件,等级{bin_item}.')
                        raster_reclassify_path = srtm_path_list[dem_productions_index]

            IXGBR.MergeRegressionClassify(predict_folder, raster_reclassify_path, merge_output_folder,
                                          _dem_type=dem_item,
                                          _year=2019)