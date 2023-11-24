# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/14 下午3:27
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
    rgi_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\1_GlaciersRegion\1_GlaciersRegion.shp"
    # 基准DEM
    dem_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\4_BaseSRTMDEM'
    dem_path_list, dem_name_list = PGF.PathGetFiles(dem_folder, '.tif')
    # SRTM数据
    dem_productions_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions'
    dem_productions_path_list, dem_productions_name_list = PGF.PathGetFiles(dem_productions_folder, '.tif')
    # 公共数据
    # 公共数据只有projx projy
    common_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\CommonData'
    common_path_list, common_name_list = PGF.PathGetFiles(common_folder, '.tif')
    # Point数据
    point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\11_Merge_Point'
    point_path_list, point_name_list = PGF.PathGetFiles(point_folder, '.shp')

    """
    PART 1
    """
    # 先循环NASA，再循环SRTM
    xgboost_output_folder = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\12_XGBoost_Data"
    # 循环DEM， 先NASA，再SRTM
    bin_list = ['B50', 'B100', 'B150', 'B200']
    bin_num_list = ['50', '100', '150', '200']
    ctype_list_abb = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10']
    ctype_list = ['Minus5', 'Minus10', 'Plus5', 'Plus10', 'Random5', 'Random10']
    for ctype_abb_index, ctype_abb_item in enumerate(ctype_list_abb):
        for bin_index, bin_item in enumerate(bin_list):
            # 寻找Point
            point_path = None
            for point_name_index, point_name_item in enumerate(point_name_list):
                if 'SRTM' in point_name_item and bin_item in point_name_item and ctype_abb_item in point_name_item:
                    point_path = point_path_list[point_name_index]
                    print(f'当前执行条件为:SRTM {bin_item} {ctype_abb_item}'
                          f'已找到文件名为:{point_name_item}')
                    break
                else:
                    print(f'未找到SRTM {bin_item} {ctype_abb_item}的Point文件.')
            slope_path, aspect_path, undulation_path, reclassify_path = None, None, None, None
            raster_projx_path, raster_projy_path = None, None
            for proj_index, proj_item in enumerate(common_name_list):
                if 'X' in proj_item:
                    raster_projx_path = common_path_list[proj_index]
                    print(f'已经找到Proj X文件')
                elif 'Y' in proj_item:
                    raster_projy_path = common_path_list[proj_index]
                    print(f'已经找到Proj Y文件')
            for dem_productions_index, dem_productions_item in enumerate(dem_productions_name_list):
                if ctype_list[ctype_abb_index] in dem_productions_item and 'Aspect' in dem_productions_item:
                    aspect_path = dem_productions_path_list[dem_productions_index]
                    print(f'Aspect {ctype_list[ctype_abb_index]}已找到.')
                elif ctype_list[ctype_abb_index] in dem_productions_item and 'Slope' in dem_productions_item:
                    slope_path = dem_productions_path_list[dem_productions_index]
                    print(f'Slope {ctype_list[ctype_abb_index]}已找到.')
                elif ctype_list[ctype_abb_index] in dem_productions_item and 'Undulation' in dem_productions_item:
                    undulation_path = dem_productions_path_list[dem_productions_index]
                    print(f'Undulation {ctype_list[ctype_abb_index]}已找到.')
                elif ctype_list[
                    ctype_abb_index] in dem_productions_item and f'Reclassify{bin_num_list[bin_index]}' in dem_productions_item:
                    reclassify_path = dem_productions_path_list[dem_productions_index]
                    print(f'Reclassify{bin_num_list[bin_index]} {ctype_list[ctype_abb_index]}已找到.')

            # 生成输出预测结果的路径
            xgboost_output_path = os.path.join(xgboost_output_folder, f'SRTM_{bin_item}_{ctype_abb_item}')
            if os.path.exists(xgboost_output_path):
                shutil.rmtree(xgboost_output_path)
                print('正在删除已存在文件夹')
            os.makedirs(xgboost_output_path)
            print(f'已创建SRTM_{bin_item}_{ctype_abb_item}的输出文件夹.')

            print(f"当前文件路径:\n"
                  f"输出路径:{xgboost_output_path}\n"
                  f"Point:{point_path}\n"
                  f"Slope:{slope_path}\n"
                  f"Aspect:{aspect_path}\n"
                  f"Undulation:{undulation_path}\n"
                  f"Reclassify:{reclassify_path}\n"
                  f"ProjX:{raster_projx_path}\n"
                  f"ProjY:{raster_projy_path}\n")

            x_var = [f'Slp_{ctype_abb_item}', f'Asp_{ctype_abb_item}', f'Und_{ctype_abb_item}', 'Proj_X', 'Proj_Y']
            y_var = [f'DH_{ctype_abb_item}']
            bin_level = f'{bin_item}_{ctype_abb_item}'

            # 开始执行预测
            IXGBR.IntegrationMultipleXGBoostRegression(point_path,
                                                       x_var,
                                                       y_var,
                                                       bin_level,
                                                       ctype_abb_item,
                                                       _output_path=xgboost_output_path,
                                                       _raster_slope_path=slope_path,
                                                       _raster_undulation_path=undulation_path,
                                                       _raster_aspect_path=aspect_path,
                                                       _raster_reclassify_path=reclassify_path,
                                                       _raster_projx_path=raster_projx_path,
                                                       _raster_projy_path=raster_projy_path)
