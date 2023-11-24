# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/13 上午10:21
# @Author : Hexk
# @Descript : 根据部分栅格值，制作调整后的DEM，用简单的相加和相减。
import random

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    srtm_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\0_PreTest_BaseData\4_BaseSRTMDEM\SRTM\SRTM_DEM.tif"
    srtm_modify5_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240513_1_RasterizeRegion\20240513_1_SRTM_Modify5.tif"
    srtm_modify10_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\20240513_1_RasterizeRegion\20240513_1_SRTM_Modify10.tif"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\4_BaseSRTMDEM'

    srtm_rr = RR.ReadRaster(srtm_path)
    srtm_data = srtm_rr.ReadRasterFile()
    srtm_modify5_rr = RR.ReadRaster(srtm_modify5_path)
    srtm_modify10_rr = RR.ReadRaster(srtm_modify10_path)
    srtm_modify5_data = srtm_modify5_rr.ReadRasterFile()
    srtm_modify10_data = srtm_modify10_rr.ReadRasterFile()

    # 5次实验，加5减5，加10减10以及一次随机±5
    srtm_plus_modify5_data = srtm_modify5_data + srtm_data
    srtm_minus_modify5_data = srtm_data - srtm_modify5_data
    srtm_minus_modify10_data = srtm_data - srtm_modify10_data
    srtm_plus_modify10_data = srtm_data + srtm_modify10_data
    random_array5 = np.empty(srtm_data.shape, dtype=float)
    random_array10 = np.empty(srtm_data.shape, dtype=float)
    for y in range(srtm_rr.raster_ds_y_size):
        for x in range(srtm_rr.raster_ds_x_size):
            if srtm_modify5_data[y][x] != 0:
                random_num = random.uniform(-5, 5)
                random_array5[y][x] = random_num + srtm_data[y][x]
            else:
                random_array5[y][x] = srtm_data[y][x]
    for y in range(srtm_rr.raster_ds_y_size):
        for x in range(srtm_rr.raster_ds_x_size):
            if srtm_modify10_data[y][x] != 0:
                random_num = random.uniform(-10, 10)
                random_array10[y][x] = random_num + srtm_data[y][x]
            else:
                random_array10[y][x] = srtm_data[y][x]
    # 写出栅格
    srtm_plus_modify5_outputpath = os.path.join(output_folder, 'srtm_plus_modify5.tif')
    srtm_minus_modify5_outputpath = os.path.join(output_folder, 'srtm_minus_modify5.tif')
    srtm_minus_modify10_outputpath = os.path.join(output_folder, 'srtm_minus_modify10.tif')
    srtm_plus_modify10_outputpath = os.path.join(output_folder, 'srtm_plus_modify10.tif')
    srtm_random5_outputpath = os.path.join(output_folder, 'srtm_random5.tif')
    srtm_random10_outputpath = os.path.join(output_folder, 'srtm_random10.tif')

    srtm_rr.WriteRasterFile(srtm_plus_modify5_data, srtm_plus_modify5_outputpath)
    srtm_rr.WriteRasterFile(srtm_minus_modify5_data, srtm_minus_modify5_outputpath)
    srtm_rr.WriteRasterFile(srtm_minus_modify10_data, srtm_minus_modify10_outputpath)
    srtm_rr.WriteRasterFile(srtm_plus_modify10_data, srtm_plus_modify10_outputpath)
    srtm_rr.WriteRasterFile(random_array5, srtm_random5_outputpath)
    srtm_rr.WriteRasterFile(random_array10, srtm_random10_outputpath)
