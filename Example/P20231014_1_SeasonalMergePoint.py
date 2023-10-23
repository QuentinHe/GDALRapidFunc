# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/14 10:31
# @Author : Hexk
# @Descript : 按照今日新理论设计进行调整，采用滑动窗口扩充每个月的数据量，将4次采样量和其他月份少量数据进行扩容
# 1 4 7 10是采样月，其他月份使用这些月份的观测计算，2月是123月之和，3月是234月之和，以此类推，12月是11 12 1月之和。这样就解决了数据点少的问题。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles
import PathOperation.PathGetFolders as PGFolders
import PathOperation.PathFilesOperation as PFO
import VectorAnalysis.ShapeMergePoint as SMP

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

# 融合shp文件
if __name__ == '__main__':
    # 批量处理的shape主文件夹
    shape_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\12_SeasonalPoint'
    # 输出结果文件夹
    shape_point_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\13_MergeSeasonalPoint'
    # 获取当前目录下的所有第一级文件夹
    main_folder_path_list, main_folder_name_list = PGFolders.PathGetFolders(shape_point_folder)
    # 次文件夹字典，用main name来当key，内容存放path和name
    sec_folder_path_dict, sec_folder_name_dict = dict(), dict()
    for main_folder_name_index, main_folder_name_item in enumerate(main_folder_name_list):
        # 次级中存files path和name
        sec_folder_path_dict[main_folder_name_item], sec_folder_name_dict[main_folder_name_item] = PGFiles.PathGetFiles(
            main_folder_path_list[main_folder_name_index], '.shp'
        )
    # 开始设定合并规则
    for main_folder_name_index, main_folder_name_item in enumerate(main_folder_name_list):
        for sec_folder_name_index, sec_folder_name_item in enumerate(sec_folder_name_dict[main_folder_name_item]):
            month = int(sec_folder_name_item.rsplit('_', 1)[1][5:])
            if month in [1, 4, 7, 10]:
                # 复制文件
                file_name = sec_folder_name_item
                file_path = sec_folder_path_dict[main_folder_name_item][sec_folder_name_index]
                output_file_folder = os.path.join(shape_point_output_folder, file_name)
                # 原文件夹
                origin_folder = file_path.rsplit('\\', 1)[0]
                PFO.CopyFolder(origin_folder, output_file_folder)
                # 复制整个文件夹
            elif month == 12:
                file_name = sec_folder_name_item
                file_path = sec_folder_path_dict[main_folder_name_item][sec_folder_name_index]
                # output_file_folder = os.path.join(shape_point_output_folder, file_name)
                # PFO.MakeFolder(output_file_folder)
                # print(output_file_folder)
                # 找到其他文件
                before_month = month - 1
                next_month = 1
                point_path_1, point_path_2 = None, None
                for temp_index, temp_item in enumerate(sec_folder_name_dict[main_folder_name_item]):
                    temp_month = temp_item.rsplit('_', 1)[1]
                    if f'Month{before_month}' == temp_month:
                        point_path_1 = sec_folder_path_dict[main_folder_name_item][temp_index]
                    if f'Month{next_month}' == temp_month:
                        point_path_2 = sec_folder_path_dict[main_folder_name_item][temp_index]
                other_point_paths_tuple = (point_path_1, point_path_2,)
                SMP.ShapeMergePoint(file_path, shape_point_output_folder, file_name, *other_point_paths_tuple)
            else:
                file_name = sec_folder_name_item
                file_path = sec_folder_path_dict[main_folder_name_item][sec_folder_name_index]
                # output_file_folder = os.path.join(shape_point_output_folder, file_name)
                # PFO.MakeFolder(output_file_folder)
                before_month = month - 1
                next_month = month + 1
                point_path_1, point_path_2 = None, None
                for temp_index, temp_item in enumerate(sec_folder_name_dict[main_folder_name_item]):
                    temp_month = temp_item.rsplit('_', 1)[1]
                    if f'Month{before_month}' == temp_month:
                        point_path_1 = sec_folder_path_dict[main_folder_name_item][temp_index]
                    if f'Month{next_month}' == temp_month:
                        point_path_2 = sec_folder_path_dict[main_folder_name_item][temp_index]
                other_point_paths_tuple = (point_path_1, point_path_2,)
                SMP.ShapeMergePoint(file_path, shape_point_output_folder, file_name, *other_point_paths_tuple)
