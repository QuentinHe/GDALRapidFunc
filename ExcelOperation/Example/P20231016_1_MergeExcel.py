# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/16 13:52
# @Author : Hexk
# @Descript : 融合同一类型的表格，包括csv excel等
import re

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    excel_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231014_Seasonal\2_PredictData\0_XGBoostData\0_ValidationResultCSV'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231014_Seasonal\2_PredictData\0_XGBoostData'
    output_path = os.path.join(output_folder, 'ValidationResultCSV.csv')
    csv_path_list, csv_name_list = PGFiles.PathGetFiles(excel_folder, '.csv')
    output_csv_dict = dict(
        NAME=[],
        R2=[],
        MSE=[],
        RMSE=[],
    )
    output_df = pd.DataFrame(output_csv_dict)
    for csv_path_index, csv_path_item in enumerate(csv_path_list):
        csv_name_list = csv_path_item.rsplit('\\', 2)[1].split('_')
        month = re.findall(r'\d+\.?\d*', csv_name_list[4])
        csv_name = f'{csv_name_list[0]}_{csv_name_list[3]}_Season{month[0]}_Lv{csv_name_list[6]}'
        csv_df = pd.read_csv(csv_path_item)
        output_df.loc[len(output_df.index)] = [csv_name, csv_df['R2'][0], csv_df['MSE'][0], csv_df['RMSE'][0]]
    output_df.to_csv(output_path)