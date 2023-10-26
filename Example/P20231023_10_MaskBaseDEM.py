# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/23 13:40
# @Author : Hexk
# @Descript : 按照RGI边界掩膜BaseDEM，并且掩膜之后加上DEM变化量，之后求解冰川厚度
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import RasterAnalysis.RasterShapeMaskRaster as RSMR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'



if __name__ == '__main__':
    raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_BaseDEM\SRTM_DEM\SRTM_DEM.tif"
    shape_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\0_BaseRegion\1_GlaciersRegion\1_GlaciersRegion.shp"
    output_raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\5_GlaciersDepth\1_MaskDEM'
    RSMR.RasterShapeMaskRaster(shape_path, raster_path, output_raster_folder)

