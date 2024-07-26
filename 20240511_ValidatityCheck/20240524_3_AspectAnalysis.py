# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/24 上午11:43
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    aspect_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240516\20_Aspect\20240524_AspectLevelClipMask.tif"
    predict_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\4_MeanData\SRTM_2019\SRTM_2019.tif'
    aspect_rr = RR.ReadRaster(aspect_path)
    aspect_data = aspect_rr.ReadRasterFile()
    predict_rr = RR.ReadRaster(predict_path)
    predict_data = predict_rr.ReadRasterFile()
    aspect_dict = dict()
    for i in range(9):
        aspect_dict[i] = []
    for y in range(predict_rr.raster_ds_y_size):
        for x in range(predict_rr.raster_ds_x_size):
            aspect_dict[aspect_data[y][x]].append(predict_data[y][x])
    aspect_list = []
    for i in range(9):
        aspect_list.append(np.mean(aspect_dict[i]))
    print(aspect_list)