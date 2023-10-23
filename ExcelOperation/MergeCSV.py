# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/23 10:00
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def MergeCSV(_csv_path_list, _output_csv_path, _merge_field=None):
    """
    融合CSV文件，按照列并列融合，可以选择其他文件中融合的字段，可以选择多个，会自动重命名，格式为 文件名+字段名；第一个文件的所有字段会保留
    :param _csv_path_list: csv文件路径，list格式
    :param _output_csv_path: 输出的csv文件路径
    :param _merge_field: 选择需要融合的字段
    :return: None
    """
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
