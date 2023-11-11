# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/13 15:30
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterClipByExtent(_raster_path, _output_raster_path, _extent=None, _clip_shape_path=None):
    """
    按照给定的范围进行栅格的裁剪，也可以输入一个shp文件，根据shp的四至进行裁剪
    :param _raster_path: 栅格文件的路径
    :param _output_raster_path: 输出栅格的路径
    :param _extent: 输入的四至点， list格式[经度min 经度max 纬度min 纬度max]
    :param _clip_shape_path: 输入shp的路径
    :return: None
    """
    # _x_min, _x_max, _y_min, _y_max = 经度min 经度max 纬度min 纬度max
    print(''.center(30, '*'))
    print('正在执行RasterClipByExtent'.center(30, '-'))
    _x_min, _x_max, _y_min, _y_max = None, None, None, None
    if _extent:
        _x_min, _x_max, _y_min, _y_max = _extent
    elif _clip_shape_path:
        shape_ds = ogr.Open(_clip_shape_path)
        layer = shape_ds.GetLayer(0)
        shape_extent = layer.GetExtent()
        _x_min, _x_max, _y_min, _y_max = shape_extent
    else:
        print('ERROR:未输入裁剪范围.'.center(30, ' '))
    print(f'裁剪范围:[{_x_min, _x_max, _y_min, _y_max}]')
    raster_rr = RR.ReadRaster(_raster_path)
    raster_data = raster_rr.ReadRasterFile()
    x_origin = raster_rr.raster_ds_geotrans[0]
    y_origin = raster_rr.raster_ds_geotrans[3]
    pixel_width = raster_rr.raster_ds_geotrans[1]
    pixel_height = raster_rr.raster_ds_geotrans[5]
    # 计算裁剪窗口的栅格
    x_start = int(np.floor((_x_min - x_origin) / pixel_width))
    x_end = int(np.ceil((_x_max - x_origin) / pixel_width))
    y_start = int(np.floor((y_origin - _y_max) / np.abs(pixel_height)))
    y_end = int(np.ceil((y_origin - _y_min) / np.abs(pixel_height)))
    clipped_data = raster_data[y_start:y_end, x_start:x_end]
    driver = gdal.GetDriverByName('GTiff')
    clipped_ds = driver.Create(_output_raster_path, x_end - x_start, y_end - y_start, 1, gdal.GDT_Float32)
    clipped_ds.SetProjection(raster_rr.raster_ds_proj)
    clipped_ds.SetGeoTransform([_x_min, pixel_width, 0, _y_max, 0, pixel_height])
    clipped_band = clipped_ds.GetRasterBand(1)
    clipped_band.SetNoDataValue(0)
    clipped_band.WriteArray(clipped_data)
    clipped_ds.FlushCache()
    del clipped_ds
    print('裁剪完成.'.center(30, ' '))
    print(''.center(30, '*'))
    return None


if __name__ == '__main__':
    raster_folder = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231112_1_WorldClim"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231113_1_WorldClimProcess'
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    for raster_index, raster_item in enumerate(raster_path_list):
        clip_name = raster_name_list[raster_index]
        output_clip_path = os.path.join(output_folder, f'{clip_name}.tif')
        RasterClipByExtent(raster_item, output_clip_path, _extent=[90, 92, 33, 34])
