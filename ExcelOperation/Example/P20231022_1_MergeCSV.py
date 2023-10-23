# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/22 20:45
# @Author : Hexk
# @Descript :
import shutil

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def MergeCSV(_csv_path_list, _output_csv_path, _merge_field=None):
    if len(_csv_path_list) != 0 and len(_csv_path_list) != 1:
        csv_df = pd.DataFrame()
        for path_index, path_item in enumerate(_csv_path_list):
            _csv_name = os.path.splitext(os.path.split(path_item)[1])[0]
            df = pd.read_csv(path_item)
            if _merge_field:
                if path_index == 0:
                    csv_df = pd.concat([csv_df, df], axis=1)
                else:
                    temp_df = df[_merge_field]
                    new_column_name = []
                    for i in temp_df.columns:
                        new_column_name.append(f'{_csv_name}_{i}')
                    temp_df.columns = new_column_name
                    csv_df = pd.concat([csv_df, temp_df], axis=1)
            else:
                temp_df = df[_merge_field]
                new_column_name = []
                for i in temp_df.columns:
                    new_column_name.append(f'{_csv_name}_{i}')
                temp_df.columns = new_column_name
                csv_df = pd.concat([csv_df, df], axis=1)
        csv_df.to_csv(_output_csv_path)
    return None


if __name__ == '__main__':
    csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\4_AnalysisRaster\3_AnalysisCSV'
    csv_path_list, csv_name_list = PGFiles.PathGetFiles(csv_folder, '.csv')
    srtm_path_list, srtm_name_liat = [], []
    nasa_path_list, nasa_name_liat = [], []
    for index, item in enumerate(csv_name_list):
        if 'NASA' in item:
            nasa_path_list.append(csv_path_list[index])
            nasa_name_liat.append(item)
        else:
            srtm_path_list.append(csv_path_list[index])
            srtm_name_liat.append(item)
    if os.path.exists(os.path.join(csv_folder, 'SRTM_SeasonalChange')):
        shutil.rmtree(os.path.join(csv_folder, 'SRTM_SeasonalChange'))
    os.makedirs(os.path.join(csv_folder, 'SRTM_SeasonalChange'))
    output_path = os.path.join(csv_folder, 'SRTM_SeasonalChange', 'SRTM_SeasonalChange.csv')
    MergeCSV(srtm_path_list, output_path, ['Mean'])

    if os.path.exists(os.path.join(csv_folder, 'NASA_SeasonalChange')):
        shutil.rmtree(os.path.join(csv_folder, 'NASA_SeasonalChange'))
    os.makedirs(os.path.join(csv_folder, 'NASA_SeasonalChange'))
    output_path = os.path.join(csv_folder, 'NASA_SeasonalChange', 'NASA_SeasonalChange.csv')
    MergeCSV(srtm_path_list, output_path, ['Mean'])
    pass
