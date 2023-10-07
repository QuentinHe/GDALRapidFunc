# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/7 9:47
# @Author : Hexk
# @Descript : 循环预测所有的分级结果

import shutil
import PathOperation.PathGetFiles as PGF
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import os

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
    nasa_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BasePoint\NASA'
    srtm_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BasePoint\SRTM'
    nasa_point_path_list, nasa_point_files_list = PGF.PathGetFiles(nasa_point_folder, '.shp')
    srtm_point_path_list, srtm_point_files_list = PGF.PathGetFiles(srtm_point_folder, '.shp')

    """
    PART 1
    """
    # 先循环NASA，再循环SRTM
    # 循环年份
    # 循环某一年的bin
    xgboost_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\1_PredictData\1_XGBoostData'
    # 循环DEM， 先NASA，再SRTM
    for dem_index, dem_item in enumerate(dem_path_list):
        dem_type = dem_files_list[dem_index].split('_')[0]  # NASA or SRTM
        # dem_type = 'SRTM'
        # 循环年份
        for year_index, year_item in enumerate([i for i in range(2019, 2023)]):
            # 循环Bin等级
            for bin_index, bin_item in enumerate([i * 50 for i in range(1, 5)]):
                # 寻找Point File Path
                point_path = None
                if dem_type == 'NASA':
                    print('正在执行NASA部分...')
                    # 找到对应的point_path
                    for point_files_index, point_files_item in enumerate(nasa_point_files_list):
                        if dem_type in point_files_item and str(
                                year_item) in point_files_item and f'Bin_{bin_item}' in point_files_item:
                            print(f'当前执行条件为:{dem_type} {year_item} {bin_item}'
                                  f'已找到文件名为:{point_files_item}')
                            point_path = nasa_point_path_list[point_files_index]
                            break
                        else:
                            print(f'ERROR: 不存在符合条件为:{dem_type} {year_item} {bin_item}的Point Shape文件.*')
                elif dem_type == 'SRTM':
                    print('正在执行SRTM部分...')
                    # 找到对应的point_path
                    for point_files_index, point_files_item in enumerate(srtm_point_files_list):
                        if dem_type in point_files_item and str(
                                year_item) in point_files_item and f'Bin_{bin_item}' in point_files_item:
                            print(f'当前执行条件为:{dem_type} {year_item} {bin_item}'
                                  f'已找到文件名为:{point_files_item}')
                            point_path = srtm_point_path_list[point_files_index]
                            break
                        else:
                            print(f'ERROR: 不存在符合条件为:{dem_type} {year_item} {bin_item}的Point Shape文件.')
                else:
                    print('dem_type存在错误，请检查基准DEM的命名。')

                # 生成bin字段
                bin_level = f'Bin_{bin_item}'

                # 生成输出预测结果的路径
                xgboost_output_path = os.path.join(xgboost_output_folder, f'{dem_type}_{year_item}_{bin_level}')
                if os.path.exists(xgboost_output_path):
                    shutil.rmtree(xgboost_output_path)
                    print('正在删除已存在文件夹')
                os.makedirs(xgboost_output_path)
                print(f'已创建{dem_type}_{year_item}_{bin_level}的输出文件夹.')

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
                if dem_type == 'NASA' or 'nasa':
                    print('正在寻找NASA的相关DEM产品路径...')
                    for dem_productions_index, dem_productions_item in enumerate(nasa_files_list):
                        if 'Slope' in dem_productions_item:
                            print(f'已经找到{dem_type}的Slope文件.')
                            raster_slope_path = nasa_path_list[dem_productions_index]
                        elif 'Aspect' in dem_productions_item:
                            print(f'已经找到{dem_type}的Aspect文件.')
                            raster_aspect_path = nasa_path_list[dem_productions_index]
                        elif 'Undulation' in dem_productions_item:
                            print(f'已经找到{dem_type}的Undulation文件.')
                            raster_undulation_path = nasa_path_list[dem_productions_index]
                        elif 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
                            print(f'已经找到{dem_type}的Reclassify文件,等级{bin_item}.')
                            raster_reclassify_path = nasa_path_list[dem_productions_index]
                elif dem_type == 'SRTM' or 'srtm':
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
                      f"Slope:{raster_slope_path}\n"
                      f"Aspect:{raster_aspect_path}\n"
                      f"Undulation:{raster_undulation_path}\n"
                      f"Reclassify:{raster_reclassify_path}\n"
                      f"ProjX:{raster_projx_path}\n"
                      f"ProjY:{raster_projy_path}\n")
                # 开始执行预测
                IXGBR.IntegrationXGBoostRegression(point_path,
                                                   ['Slope', 'Aspect', 'Undulation', 'Proj_X', 'Proj_Y'],
                                                   ['Delta_Ele'],
                                                   bin_level,
                                                   _output_path=xgboost_output_path,
                                                   _raster_slope_path=raster_slope_path,
                                                   _raster_undulation_path=raster_undulation_path,
                                                   _raster_aspect_path=raster_aspect_path,
                                                   _raster_reclassify_path=raster_reclassify_path,
                                                   _raster_projx_path=raster_projx_path,
                                                   _raster_projy_path=raster_projy_path)
