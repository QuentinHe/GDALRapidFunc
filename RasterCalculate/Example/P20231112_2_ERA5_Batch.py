# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/12 10:45
# @Author : Hexk
# @Descript : ERA5数据合并
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231112_1_ERA5_Raster'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231112_2_ERA5_Merge'
    year_list = [i for i in range(2000, 2023)]
    month_list = [i for i in range(1, 13)]
    type_list = ['t2m', 'tp']
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    for type_index, type_item in enumerate(type_list):
        target_result_list = None
        type_df = pd.DataFrame(columns=['Type', 'Year', 'Month', 'Max', 'Min', 'Mean'])
        for year_index, year_item in enumerate(year_list):
            # for month_index, month_item in enumerate(month_list):
            target_result_list = [i for i in raster_path_list if str(type_item) in i and str(year_item) in i]
            # 计算月平均降水和月平均气温，输出成一个excel
            for raster_index, raster_item in enumerate(target_result_list):
                month = os.path.splitext(os.path.split(raster_item)[1])[0].rsplit('_', 2)[1]
                temp_rr = RR.ReadRaster(raster_item)
                temp_data = temp_rr.ReadRasterFile()
                temp_data_list = temp_data.reshape(-1)
                temp_mean = np.mean(temp_data_list)
                temp_max = np.max(temp_data_list)
                temp_min = np.min(temp_data_list)
                temp_df = pd.DataFrame([{
                    'Type': type_item,
                    'Year': year_item,
                    'Month': month,
                    'Max': temp_max,
                    'Min': temp_min,
                    'Mean': temp_mean
                }])
                type_df = pd.concat([type_df, temp_df], axis=0)
            output_excel_path = os.path.join(output_folder, f'{type_item}_{year_list[0]}_{year_list[-1]}.xlsx')
            type_df.to_excel(output_excel_path)
