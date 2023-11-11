# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/12 10:45
# @Author : Hexk
# @Descript : ERA5数据合并
import os
import PathOperation.PathGetFiles as PGFiles
import RasterCalculate.RasterCalculator as RC

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231112_1_ERA5_Raster'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231111_1_ERA5\20231113_2_ERA5_RasterMerge'
    year_list = [i for i in range(2000, 2023)]
    month_list = [i for i in range(1, 13)]
    type_list = ['t2m', 'tp']
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    for type_index, type_item in enumerate(type_list):
        target_result_list = None
        for year_index, year_item in enumerate(year_list):
            # for month_index, month_item in enumerate(month_list):
            target_result_list = [i for i in raster_path_list if str(type_item) in i and str(year_item) in i]
            # 计算年平均气温和年平均降水
            # for raster_index, raster_item in enumerate(target_result_list):
                # month = os.path.splitext(os.path.split(raster_item)[1])[0].rsplit('_', 2)[1]
            RC.RasterAdd(target_result_list[0], output_folder, *target_result_list[1:], _output_name=f'{type_item}_Sum_{year_item}')



