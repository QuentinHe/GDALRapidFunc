# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/17 下午4:17
# @Author : Hexk
# @Descript :
import PathOperation.PathGetFiles as PGF
import PathOperation.PathFilesOperation as PFO
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR
import numpy as np
import ErrorAnalysis.ErrorAnalysis as EA
import os
import pandas as pd
import matplotlib.pyplot as plt

from RasterAnalysis.RasterClipByShape import RasterClipByShape

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    # 计算全区域分级
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\16_MaskResult'
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\14_Mask\Mask_M5\Reclassify\Reclassify.tif"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\18_OutputExcel'
    reclassify_rr = RR.ReadRaster(reclassify_path)
    reclassify_data = reclassify_rr.ReadRasterFile()
    raster_path_list, raster_name_list = PGF.PathGetFiles(raster_folder, '.tif')
    output_df = pd.DataFrame()
    for raster_name_index, raster_name_item in enumerate(raster_name_list):
        bins_dict = dict()
        temp_rr = RR.ReadRaster(raster_path_list[raster_name_index])
        temp_data = temp_rr.ReadRasterFile()
        for i in range(17):
            bins_dict[i] = []
        for y in range(reclassify_rr.raster_ds_y_size):
            for x in range(reclassify_rr.raster_ds_x_size):
                bins_dict[reclassify_data[y][x]].append(temp_data[y][x])
        bins_mean_list = []
        for i in range(len(bins_dict.keys())):
            bins_mean_list.append(np.mean(bins_dict[i]))
        output_df[raster_name_item] = bins_mean_list
    output_path = os.path.join(output_folder, 'OutputExcel.xlsx')
    output_df.to_excel(output_path)
