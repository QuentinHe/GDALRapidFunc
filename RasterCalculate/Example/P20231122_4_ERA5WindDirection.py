# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/22 11:01
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231122_1_ERA5Wind\20231122_2_WindTifAdd'
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231122_1_ERA5Wind\20231122_4_WindTifDirection'
    u10_rr = None
    u10_data = None
    v10_rr = None
    v10_data = None
    for index, item in enumerate(raster_name_list):
        name = os.path.splitext(item)[0].rsplit('_', 1)[1]
        if 'u10' == name:
            u10_rr = RR.ReadRaster(raster_path_list[index])
            u10_data = u10_rr.ReadRasterFile()
        elif 'v10' == name:
            v10_rr = RR.ReadRaster(raster_path_list[index])
            v10_data = v10_rr.ReadRasterFile()
    # 计算方向
    # v是 北正南负
    # u是 东正西负
    result_data = np.empty((v10_rr.raster_ds_y_size, v10_rr.raster_ds_x_size))
    for y in range(v10_rr.raster_ds_y_size):
        for x in range(v10_rr.raster_ds_x_size):
            direction = np.arctan(u10_data[y][x] / v10_data[y][x]) / np.pi * 180
            result_data[y][x] = direction
    output_path = os.path.join(output_folder, '20231122_4_WindTifDirection.tif')
    v10_rr.WriteRasterFile(result_data, output_path, _nodata=0)
