# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/15 上午10:06
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGF
import ReadRasterAndShape.ReadRaster as RR
import RasterAnalysis.RasterClipByShape as RCBS

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\14_Mask_Data'
    shape_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240512_1_ModifyRegionShape\20240512_2_CutRegion.shp"
    output_folder =r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\20240515_1_ClipRaster'
    raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\4_MeanData\SRTM_2019\SRTM_2019.tif'
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\3_MaskData\Mask_SRTM_2019_Bin_50\Mask_SRTM_2019_Bin_50\Reclassify\Reclassify.tif"
    bins = 'B50'
    ctype_list = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10']
    # raster_path_list, raster_name_list = PGF.PathGetFiles(raster_folder, '.tif')
    # for name_index, name_item in enumerate(raster_name_list):
    #     output_path = os.path.join(output_folder, f'Clip_{name_item}.tif')
    #     RCBS.RasterClipByShape(shape_path, raster_path_list[name_index], output_path)
    output_path = os.path.join(output_folder, f'Clip_Predict_Reclassify.tif')
    RCBS.RasterClipByShape(shape_path, reclassify_path, output_path)
