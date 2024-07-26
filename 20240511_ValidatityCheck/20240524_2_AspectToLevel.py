# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/24 上午11:23
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    aspect_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\20_Aspect\20240524_Aspect.tif'
    aspect_rr = RR.ReadRaster(aspect_path)
    aspect_data = aspect_rr.ReadRasterFile()
    output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\20_Aspect\20240524_AspectLevel.tif'
    aspect_level_data = np.empty(aspect_data.shape)
    for y in range(aspect_rr.raster_ds_y_size):
        for x in range(aspect_rr.raster_ds_x_size):
            value = np.ceil(aspect_data[y][x] / 45)
            if value <= 0 or value > 8:
                aspect_level_data[y][x] = 0
            else:
                aspect_level_data[y][x] = value
    aspect_rr.WriteRasterFile(aspect_level_data, output_path)
