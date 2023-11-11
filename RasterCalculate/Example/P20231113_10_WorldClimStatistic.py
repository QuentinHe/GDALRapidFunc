# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/13 20:33
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles
import RasterCalculate.RasterCalculator as RC
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_1_WorldClimProcess'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_2_WorldClimProcessResult\20231113_4_WCPR_Excel'
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    type_list = ['prec', 'tmax', 'tmin']
    year_list = [i for i in range(2000, 2022)]
    month_list = [i for i in range(1, 13)]
    df_list = []
    for type_index, type_item in enumerate(type_list):
        result_df = pd.DataFrame(columns=['Year', f'{type_item}_Mean'])
        for year_index, year_item in enumerate(year_list):
            temp_raster_tuple = list(zip(range(len(raster_path_list)), raster_path_list))
            temp_filter_raster_tuple = list(
                filter(lambda x: str(type_item) in x[1] and str(year_item) in x[1], temp_raster_tuple))
            temp_result_list = list(list(zip(*temp_filter_raster_tuple))[1])
            # 统计四个表格，年变化 月变化各两个
            # 先统计年变化
            mean_list = []
            for raster_index, raster_item in enumerate(temp_result_list):
                raster_rr = RR.ReadRaster(raster_item)
                raster_data = raster_rr.ReadRasterFile()
                # 一幅影像的均值
                mean = np.mean(raster_data)
                mean_list.append(mean)
            temp_df = pd.DataFrame([{
                'Year': year_item,
                # 12幅影像的均值，表示一年的平均值
                f'{type_item}_Mean': np.mean(mean_list)
            }])
            result_df = pd.concat([result_df, temp_df])
        df_list.append(result_df)
    # 月变化
    for type_index, type_item in enumerate(type_list):
        result_df = pd.DataFrame(columns=['Month', f'{type_item}_Mean'])
        for month_index, month_item in enumerate(month_list):
            temp_raster_tuple = list(zip(range(len(raster_path_list)), raster_path_list))
            temp_filter_raster_tuple = list(
                filter(lambda x: str(type_item) in x[1] and int(os.path.splitext(os.path.split(x[1])[1])[0].split('-')[1]) == month_item, temp_raster_tuple))
            temp_result_list = list(list(zip(*temp_filter_raster_tuple))[1])
            mean_list = []
            for raster_index, raster_item in enumerate(temp_result_list):
                raster_rr = RR.ReadRaster(raster_item)
                raster_data = raster_rr.ReadRasterFile()
                mean = np.mean(raster_data)
                mean_list.append(mean)
            temp_df = pd.DataFrame([{
                'Month': month_item,
                f'{type_item}_Mean': np.mean(mean_list)
            }])
            result_df = pd.concat([result_df, temp_df])
        df_list.append(result_df)
    output_excel_path = os.path.join(output_folder, 'WorldClim_Result.xlsx')
    df_list[0].to_excel(output_excel_path, sheet_name='prec_Year')
    with pd.ExcelWriter(output_excel_path, engine='openpyxl', mode='a') as writer:
        df_list[1].to_excel(writer, sheet_name='tmax_Year')
        df_list[2].to_excel(writer, sheet_name='tmin_Year')
        df_list[3].to_excel(writer, sheet_name='prec_Month')
        df_list[4].to_excel(writer, sheet_name='tmax_Month')
        df_list[5].to_excel(writer, sheet_name='tmin_Month')