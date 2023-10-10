# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/7 9:49
# @Author : Hexk
# @Descript : 融合PART1的结果，按classify的类别融合

import PathOperation.PathGetFiles as PGF
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    # RGI区域
    rgi_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseRGIRegion\3_Landsat8_RGI_2020.shp"
    # 基准DEM
    dem_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEM'
    dem_path_list, dem_files_list = PGF.PathGetFiles(dem_folder, '.tif')
    # NASA数据
    nasa_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\NASA'
    nasa_path_list, nasa_files_list = PGF.PathGetFiles(nasa_folder, '.tif')
    # SRTM数据
    srtm_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\SRTM'
    srtm_path_list, srtm_files_list = PGF.PathGetFiles(srtm_folder, '.tif')
    # 公共数据
    common_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\CommonData'
    common_path_list, common_files_list = PGF.PathGetFiles(common_folder, '.tif')
    # Point数据
    # nasa_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BasePoint\NASA'
    nasa_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231008\0_BaseData\BasePoint\NASA'
    # srtm_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BasePoint\SRTM'
    srtm_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231008\0_BaseData\BasePoint\SRTM'
    nasa_point_path_list, nasa_point_files_list = PGF.PathGetFiles(nasa_point_folder, '.shp')
    srtm_point_path_list, srtm_point_files_list = PGF.PathGetFiles(srtm_point_folder, '.shp')
    """
    PART 2
    """
    # xgboost_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\1_PredictData\1_XGBoostData'
    xgboost_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231008\1_PredictData\1_XGBoostData'
    # 融合
    dem_type_list = ['NASA','SRTM']
    # years_list = [i for i in range(2019, 2023)]
    years_list = [2019]
    bin_list = [i * 50 for i in range(1, 5)]
    # merge_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\1_PredictData'
    merge_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231008\1_PredictData\2_MergeData'
    for dem_index, dem_item in enumerate(dem_type_list):
        for year_index, year_item in enumerate(years_list):
            for bin_index, bin_item in enumerate(bin_list):
                predict_folder = os.path.join(xgboost_output_folder, f'{dem_item}_{year_item}_Bin_{bin_item}')
                raster_reclassify_path = None
                if dem_item == 'NASA':
                    print('正在寻找NASA的相关DEM产品路径...')
                    for dem_productions_index, dem_productions_item in enumerate(nasa_files_list):
                        if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
                            print(f'已经找到{dem_item}的Reclassify文件,等级{bin_item}.')
                            raster_reclassify_path = nasa_path_list[dem_productions_index]
                elif dem_item == 'SRTM':
                    print('正在寻找SRTM的相关DEM产品路径...')
                    for dem_productions_index, dem_productions_item in enumerate(srtm_files_list):
                        if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
                            print(f'已经找到{dem_item}的Reclassify文件,等级{bin_item}.')
                            raster_reclassify_path = srtm_path_list[dem_productions_index]

                IXGBR.MergeRegressionClassify(predict_folder, raster_reclassify_path, merge_output_folder,
                                              _dem_type=dem_item,
                                              _year=year_item)
