# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/15 上午10:23
# @Author : Hexk
# @Descript : Clip区域所有像元的整体变化
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGF
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_2_ClipRaster'
    output_excel_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_3_ClipExcel'
    bins = 'B50'
    ctype_list = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10', 'Predict']
    raster_path_list, raster_name_list = PGF.PathGetFiles(raster_folder, '.tif')
    raster_list = []
    reclassify_list = []
    for raster_name_index, raster_name_item in enumerate(raster_name_list):
        for ctype_index, ctype_item in enumerate(ctype_list):
            if f'Clip_Mask_{bins}_{ctype_item}' in raster_name_item:
                raster_list.append(raster_path_list[raster_name_index])
            if f'Clip_Reclassify_{bins}_{ctype_item}' in raster_name_item:
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
    output_excel_path = os.path.join(output_excel_folder, 'Clip_Bin_Statistics.xlsx')
    mean_df.to_excel(output_excel_path, sheet_name='Sheet1', index=False)
