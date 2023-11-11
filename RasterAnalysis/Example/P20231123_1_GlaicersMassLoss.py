# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/23 15:04
# @Author : Hexk
# @Descript : 计算冰川的物质平衡
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\4_MeanData\SRTM_2019\SRTM_2019.tif"
    raster_rr = RR.ReadRaster(raster_path)
    raster_data = raster_rr.ReadRasterFile()
    after_item = 0
    pixel_num = 0
    for y in range(raster_rr.raster_ds_y_size):
        for x in range(raster_rr.raster_ds_x_size):
            if raster_data[y][x]:
                after_item += raster_data[y][x] * 30 * 30
                pixel_num += 1
    loss = 850 * after_item / (30 * 30 * pixel_num)
    print(loss/20)
