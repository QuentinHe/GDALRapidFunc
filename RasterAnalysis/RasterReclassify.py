# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/9 14:29
# @Author : Hexk
# @Descript : 重分类DEM

from bisect import bisect_left
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterReclassify(_raster_data, _start, _end, _space):
    bins = np.arange(_start, _end, _space)
    print(f'划分栅格值的间隔线为：{bins}, 共有{len(bins) + 1}个等级.')
    bins_level = list()
    for i in np.nditer(_raster_data):
        bins_level.append(bisect_left(bins, i) + 1)
    print(f'bins_level的长度为:{len(bins_level)},正在转换成shape{_raster_data.shape}')
    print(f'bins_level最小等级为:{min(bins_level)}, 最大等级为:{max(bins_level)}')
    bins_level = np.array(bins_level)
    bins_data = bins_level.reshape(_raster_data.shape)
    # 输出成重分类后DEM
    return bins_data


if __name__ == '__main__':
    input_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_BaseDEM\NASA_DEM\NASA_DEM.tif'
    output_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\NASA_Reclassify_200'
    raster_rr = RR.ReadRaster(input_raster_path)
    raster_data = raster_rr.ReadRasterFile()
    bins_data = RasterReclassify(raster_data, 5400, 6150, 200)
    raster_rr.WriteRasterFile(bins_data, output_raster_path)
