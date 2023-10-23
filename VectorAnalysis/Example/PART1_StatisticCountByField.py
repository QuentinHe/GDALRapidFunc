# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/13 13:49
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import VectorAnalysis.ShapePointCountStatistic as SPCS
import PathOperation.PathGetFiles as PGFiles
import PathOperation.PathGetFolders as PGFolders

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    main_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231009\0_BasePoint'
    main_folder_path_list, main_folder_name_list = PGFolders.PathGetFolders(main_folder)
    sec_folder_paths_dict = dict()
    sec_folder_name_dict = dict()
    for index, item in enumerate(main_folder_name_list):
        sec_folder_paths_dict[item], sec_folder_name_dict[item] = PGFolders.PathGetFolders(main_folder_path_list[index])
    for main_folder_index, main_folder_item in enumerate(main_folder_name_list):
        csv_df = pd.DataFrame()
        # 50 100 150 200
        classify_field = main_folder_item.rsplit('_', 1)[1]
        # 循环子文件夹dict
        for sec_folder_item in sec_folder_paths_dict[main_folder_item]:
            shape_path, shape_file = PGFiles.PathGetFiles(sec_folder_item, '.shp')
            level_count_list = SPCS.ShapeFieldClassifyCountStatistic(shape_path[0], f'Bin_{classify_field}')
            df = pd.DataFrame(level_count_list, columns=[f'{shape_file[0]}'])
            csv_df = pd.concat([csv_df, df], axis=1)
        csv_df.fillna(0)
        csv_df.loc['Sum'] = csv_df.apply(lambda x: x.sum())
        output_csv_path = os.path.join(main_folder_path_list[main_folder_index], f'{main_folder_item}_Counts.csv')
        csv_df.to_csv(output_csv_path)
