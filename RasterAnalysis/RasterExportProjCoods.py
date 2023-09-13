# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/12 10:21
# @Author : Hexk
# @Descript : 导出DEM的每个像元的投影坐标，X和Y，分别导出成两个TIF文件
import shutil

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterExportProjCoords(_input_raster_path, _output_raster_path):
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")

    if not os.path.exists(_output_raster_path):
        os.makedirs(_output_raster_path)
        print('不存在ExportProjCoords处理后的文件...')
    else:
        shutil.rmtree(_output_raster_path)
        print('ExportProjCoords处理后的文件已存在，正在删除...')
    input_rr = RR.ReadRaster(input_path=_input_raster_path)
    input_ds = input_rr.ReadRasterFile()
    proj_x_list, proj_y_list = input_rr.ReadRasterProjCoordinate()
    proj_x_data = np.array(proj_x_list).reshape(input_rr.raster_ds_y_size, input_rr.raster_ds_x_size)
    proj_y_data = np.array(proj_y_list).reshape(input_rr.raster_ds_y_size, input_rr.raster_ds_x_size)
    input_rr.WriteRasterFile(proj_x_data, os.path.join(_output_raster_path, 'ProjX'))
    input_rr.WriteRasterFile(proj_y_data, os.path.join(_output_raster_path, 'ProjY'))
    return None


if __name__ == '__main__':
    input_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_BaseDEM\NASA_DEM\NASA_DEM.tif'
    output_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\4_DEM_ProjCoords'
    RasterExportProjCoords(input_raster_path, output_raster_path)