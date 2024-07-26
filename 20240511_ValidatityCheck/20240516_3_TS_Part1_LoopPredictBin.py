# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/16 上午11:25
# @Author : Hexk
# @Descript :

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import shutil
import PathOperation.PathGetFiles as PGF
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    # RGI区域
    rgi_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\1_GlaciersRegion\1_GlaciersRegion.shp"
    # 基准DEM
    dem_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\4_BaseSRTMDEM'
    dem_path_list, dem_files_list = PGF.PathGetFiles(dem_folder, '.tif')
    # SRTM数据
    srtm_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\5_BaseDEMProductions\SRTM'
    srtm_path_list, srtm_files_list = PGF.PathGetFiles(srtm_folder, '.tif')
    # 公共数据
    # 公共数据只有projx projy
    common_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\CommonData'
    common_path_list, common_files_list = PGF.PathGetFiles(common_folder, '.tif')
    # Point数据
    point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\7_TS_PointMerge\7_TS_PointMerge.shp"

    """
    PART 1
    """
    # 先循环NASA，再循环SRTM
    xgboost_output_folder = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\8_TS_XGBoostData_R10"
    # 循环DEM， 先NASA，再SRTM
    for dem_index, dem_item in enumerate(dem_path_list):
        dem_type = dem_files_list[dem_index].split('_')[0]  # NASA or SRTM
        # dem_type = 'SRTM'
        # 循环Bin等级
        for bin_index, bin_item in enumerate([i * 50 for i in range(1, 5)]):

            # 生成bin字段
            bin_level = f'Bin_{bin_item}'

            # 生成输出预测结果的路径
            xgboost_output_path = os.path.join(xgboost_output_folder, f'{dem_type}_{bin_level}')
            if os.path.exists(xgboost_output_path):
                shutil.rmtree(xgboost_output_path)
                print('正在删除已存在文件夹')
            os.makedirs(xgboost_output_path)
            print(f'已创建{dem_type}_{bin_level}的输出文件夹.')

            # 找到其他DEM输入参数的路径
            raster_slope_path, raster_aspect_path, raster_undulation_path, raster_reclassify_path = None, None, None, None
            raster_projx_path = None
            raster_projy_path = None
            for proj_index, proj_item in enumerate(common_files_list):
                if 'X' in proj_item:
                    raster_projx_path = common_path_list[proj_index]
                    print(f'已经找到{dem_type}的Proj X文件')
                elif 'Y' in proj_item:
                    raster_projy_path = common_path_list[proj_index]
                    print(f'已经找到{dem_type}的Proj Y文件')
            if dem_type == 'SRTM' or 'srtm':
                print('正在寻找SRTM的相关DEM产品路径...')
                for dem_productions_index, dem_productions_item in enumerate(srtm_files_list):
                    if 'Slope' in dem_productions_item:
                        print(f'已经找到{dem_type}的Slope文件.')
                        raster_slope_path = srtm_path_list[dem_productions_index]
                    elif 'Aspect' in dem_productions_item:
                        print(f'已经找到{dem_type}的Aspect文件.')
                        raster_aspect_path = srtm_path_list[dem_productions_index]
                    elif 'Undulation' in dem_productions_item:
                        print(f'已经找到{dem_type}的Undulation文件.')
                        raster_undulation_path = srtm_path_list[dem_productions_index]
                    elif 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
                        print(f'已经找到{dem_type}的Reclassify文件,等级{bin_item}.')
                        raster_reclassify_path = srtm_path_list[dem_productions_index]
            else:
                print('dem_type存在错误，请检查基准DEM的命名。')

            print(f"当前文件路径:\n"
                  f"输出路径:{xgboost_output_path}\n"
                  f"Point:{point_path}\n"
                  f"Slope:{raster_slope_path}\n"
                  f"Aspect:{raster_aspect_path}\n"
                  f"Undulation:{raster_undulation_path}\n"
                  f"Reclassify:{raster_reclassify_path}\n"
                  f"ProjX:{raster_projx_path}\n"
                  f"ProjY:{raster_projy_path}\n")
            if point_path is None:
                print('Point路径不存在!')
            else:
                # 开始执行预测
                IXGBR.IntegrationXGBoostRegression(point_path,
                                                   ['Slope', 'Aspect', 'Undulation', 'Proj_X', 'Proj_Y'],
                                                   ['R10'],
                                                   bin_level,
                                                   _output_path=xgboost_output_path,
                                                   _raster_slope_path=raster_slope_path,
                                                   _raster_undulation_path=raster_undulation_path,
                                                   _raster_aspect_path=raster_aspect_path,
                                                   _raster_reclassify_path=raster_reclassify_path,
                                                   _raster_projx_path=raster_projx_path,
                                                   _raster_projy_path=raster_projy_path)
