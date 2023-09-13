# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/13 9:43
# @Author : Hexk
# @Descript : 两个栅格相减
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterReduce(_first_raster_path, _second_raster_path, _output_path):
    first_rr = RR.ReadRaster(_first_raster_path)
    second_rr = RR.ReadRaster(_second_raster_path)
    first_data = first_rr.ReadRasterFile()
    second_data = second_rr.ReadRasterFile()
    result = np.array(first_data) - np.array(second_data)
    first_rr.WriteRasterFile(result, _output_path, _nodata=0)
    return None


if __name__ == '__main__':
    first_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Analysis_Raster_Result\2_Predict_Reduce_BaseDEM_Mask_RGI\Delta_NASA_2022\Delta_NASA_2022.tif'
    second_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Analysis_Raster_Result\2_Predict_Reduce_BaseDEM_Mask_RGI\Delta_NASA_2021\Delta_NASA_2021.tif'
    output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Analysis_Raster_Result\3_MaskResult_Reduce_Predict2019\2022_Reduce_2021'
    RasterReduce(first_raster_path, second_raster_path, output_path)
