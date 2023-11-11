# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/8 15:22
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import PathOperation.PathGetFiles as PGFiles
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    excel_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231108_7_Analysis_Excel'
    excel_path_list, excel_name_list = PGFiles.PathGetFiles(excel_folder, '.xlsx')
    month_path_list, month_name_list = [], []
    for index, item in enumerate(excel_path_list):
        montly_type = excel_name_list[index].split('_')[1]
        if montly_type == '21':
            month_path_list.append(item)
            month_name_list.append(excel_name_list[index])
    output_df = pd.DataFrame()
    for index, item in enumerate(month_path_list):
        if index == 0:
            excel_name = month_name_list[index].split('_')[2]
            temp_df = pd.read_excel(item)[['ID', 'Glaciers_Name', 'PixelNums', 'Mean']]
            temp_df.rename(columns={'Mean': f'{excel_name}_Mean'}, inplace=True)
            output_df = pd.concat([output_df, temp_df], axis=1)
        else:
            excel_name = month_name_list[index].split('_')[2]
            temp_df = pd.read_excel(item)[['Mean']]
            temp_df.rename(columns={'Mean': f'{excel_name}_Mean'}, inplace=True)
            output_df = pd.concat([output_df, temp_df], axis=1)
    output_excel_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231108_7_Analysis_Excel\20231108_21_MonthSum.xlsx'
    output_df.to_excel(output_excel_path)
