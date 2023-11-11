# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/13 9:55
# @Author : Hexk
# @Descript : 20年的平均温度、平均降水统计，输出一张表格。 202年的月平均温度和平均降水统计，输出一张表格。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    t2m_excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231112_2_ERA5_Merge\t2m_2000_2022.xlsx"
    tp_excel_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231112_2_ERA5_Merge\tp_2000_2022.xlsx"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231113_1_ERA5_Result'
    t2m_df = pd.read_excel(t2m_excel_path, sheet_name='Sheet1')
    tp_df = pd.read_excel(tp_excel_path, sheet_name='Sheet1')
    year_list = [i for i in range(2000, 2023)]
    t2m_year_df = pd.DataFrame(columns=['Year', 't2m_Mean'])
    tp_year_df = pd.DataFrame(columns=['Year', 'tp_Mean'])
    for year_index, year_item in enumerate(year_list):
        t2m_temp_df = t2m_df[t2m_df['Year'].isin([year_item])]
        tp_temp_df = tp_df[tp_df['Year'].isin([year_item])]
        t2m_mean = t2m_temp_df['Mean'].mean() - 273.15
        tp_mean = tp_temp_df['Mean'].mean()
        t2m_mean_df = pd.DataFrame([{
            'Year': year_item,
            't2m_Mean': t2m_mean
        }])
        t2m_year_df = pd.concat([t2m_year_df, t2m_mean_df])
        tp_mean_df = pd.DataFrame([{
            'Year': year_item,
            'tp_Mean': tp_mean
        }])
        tp_year_df = pd.concat([tp_year_df, tp_mean_df])
    month_list = [i for i in range(1, 13)]
    t2m_month_df = pd.DataFrame(columns=['Month', 't2m_Mean'])
    tp_month_df = pd.DataFrame(columns=['Month', 'tp_Mean'])
    for month_index, month_item in enumerate(month_list):
        t2m_temp_df = t2m_df[t2m_df['Month'].isin([month_item])]
        tp_temp_df = tp_df[tp_df['Month'].isin([month_item])]
        t2m_mean = t2m_temp_df['Mean'].mean() - 273.15
        tp_mean = tp_temp_df['Mean'].mean()
        t2m_mean_df = pd.DataFrame([{
            'Month': month_item,
            't2m_Mean': t2m_mean
        }])
        t2m_month_df = pd.concat([t2m_month_df, t2m_mean_df])
        tp_mean_df = pd.DataFrame([{
            'Month': month_item,
            'tp_Mean': tp_mean
        }])
        tp_month_df = pd.concat([tp_month_df, tp_mean_df])
    output_excel_path = os.path.join(output_folder, '20231113_1_ERA5_Result.xlsx')
    t2m_year_df.to_excel(output_excel_path, sheet_name='t2m_Year')
    with pd.ExcelWriter(output_excel_path, engine='openpyxl', mode='a') as writer:
        t2m_month_df.to_excel(writer, sheet_name='t2m_Month')
        tp_year_df.to_excel(writer, sheet_name='tp_Year')
        tp_month_df.to_excel(writer, sheet_name='tp_Month')
