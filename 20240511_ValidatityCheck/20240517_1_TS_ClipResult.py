# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/17 上午10:04
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

from RasterAnalysis.RasterClipByShape import RasterClipByShape

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_folder =r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\16_MaskResult'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\17_ClipResult'
    region_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240512_1_ModifyRegionShape\20240512_2_CutRegion.shp'

    raster_list, raster_name_list = PGF.PathGetFiles(raster_folder, '.tif')
    for index, item in enumerate(raster_name_list):
        output_path = os.path.join(output_folder, f'Clip_{item}.tif')
        RasterClipByShape(region_path, raster_list[index], output_path)