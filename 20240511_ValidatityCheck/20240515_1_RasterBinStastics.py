# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/15 上午9:25
# @Author : Hexk
# @Descript : 只统计B50的Mask文件，按照Bin等级统计均值和标准差，整个研究区区域的整体变化情况
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGF
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\14_Mask_Data'
    output_excel_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\22_Raster_Bin_Stastics'
    bins = 'B50'
    ctype_list = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10']
    raster_path_list, raster_name_list = PGF.PathGetFiles(raster_folder, '.tif')

    raster_list = []
    reclassify_list = []
    for raster_name_index, raster_name_item in enumerate(raster_name_list):
        for ctype_index, ctype_item in enumerate(ctype_list):
            if f'Mask_{bins}_{ctype_item}' in raster_name_item:
                raster_list.append(raster_path_list[raster_name_index])
            if f'Reclassify_{bins}_{ctype_item}' in raster_name_item:
                reclassify_list.append(raster_path_list[raster_name_index])
    mean_df = pd.DataFrame()
    for raster_index, raster_item in enumerate(raster_list):
        bin_dict = dict()
        bin_mean_list = []
        raster_rr = RR.ReadRaster(raster_item)
        raster_data = raster_rr.ReadRasterFile()
        reclassify_rr = RR.ReadRaster(reclassify_list[raster_index])
        reclassify_data = reclassify_rr.ReadRasterFile()
        for i in range(17):
            bin_dict[i] = []
        for y in range(reclassify_rr.raster_ds_y_size):
            for x in range(reclassify_rr.raster_ds_x_size):
                bin_dict[int(reclassify_data[y][x])].append(raster_data[y][x])
        for i in range(17):
            bin_mean_list.append(np.mean(bin_dict[i]))
        field_name = os.path.splitext(raster_list[raster_index])[0].split("\\")[-1]
        temp_df = pd.DataFrame(bin_mean_list, columns=[f'{field_name}'])
        mean_df = pd.concat([mean_df, temp_df], axis=1)
    output_excel_path = os.path.join(output_excel_folder, 'Raster_Bin_Statistics.xlsx')
    mean_df.to_excel(output_excel_path, sheet_name='Sheet1', index=False)
