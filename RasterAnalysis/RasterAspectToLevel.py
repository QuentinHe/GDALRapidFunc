# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/7 16:08
# @Author : Hexk
# Aspect文件，坡向转等级

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadShape2DataFrame as RSDF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterAspectToLevel(_input_path, _output_path):
    print('正在进行坡向转等级...')
    input_rr = RR.ReadRaster(_input_path)
    input_data = input_rr.ReadRasterFile()
    input_data_list = input_data.reshape(-1)
    aspect_level_list = RSDF.AspectConvertLevel(input_data_list)
    aspect_level_data = aspect_level_list.reshape(input_rr.raster_ds_y_size, input_rr.raster_ds_x_size)
    input_rr.WriteRasterFile(_output_path, aspect_level_data)
    print('转换完成.')


if __name__ == '__main__':
    input_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\1_DEM_Aspect\SRTM_DEM\1_SRTM_Aspect.tif'
    output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\1_DEM_Aspect\SRTM_Aspect_Level\SRTM_Aspect_Level.tif'
    RasterAspectToLevel(input_path, output_path)
