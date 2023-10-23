# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/13 14:37
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFolders as PGFolders
import PathOperation.PathGetFiles as PGFiles
import VectorAnalysis.ShapeFieldStatistic as SFS

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    main_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231009\0_BasePoint'
    main_folder_dir_path, main_folder_dir_name = PGFolders.PathGetFolders(main_folder)
    sec_folder_dir_path_dict = dict()
    sec_folder_dir_name_dict = dict()
    for index, item in enumerate(main_folder_dir_path):
        sec_folder_dir_path_dict[main_folder_dir_name[index]], sec_folder_dir_name_dict[main_folder_dir_name[index]], = PGFolders.PathGetFolders(item)
        # 50 100 150 200
        classify_field = main_folder_dir_name[index].rsplit('_', 1)[1]
        csv_df = pd.DataFrame()
        total_mean_list = []
        for path_index, path_item in enumerate(sec_folder_dir_path_dict[main_folder_dir_name[index]]):
            column = sec_folder_dir_name_dict[main_folder_dir_name[index]][path_index].rsplit('_', 1)[1]
            total_mean, level_mean = SFS.ShapeFieldMean(path_item, 'Delta_Ele', _classify_field=f'Bin_{classify_field}')
            total_mean_list.append(total_mean)
            df = pd.DataFrame(level_mean, columns=[column])
            csv_df = pd.concat([csv_df, df], axis=1)
        csv_df.loc['Total_Mean'] = total_mean_list
        output_csv_path = os.path.join(item, f'{main_folder_dir_name[index]}_Delta_Elevation.csv')
        csv_df.to_csv(output_csv_path)

