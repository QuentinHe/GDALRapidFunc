# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/9 14:29
# @Author : Hexk
# @Descript : 重分类

from bisect import bisect_left
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR
import PathOperation.PathGetFiles as PGF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterReclassify(_raster_path, _raster_output_path, _classify_list=None, **kwargs):
    """
    重分类方法，该方法较为完整，后期整理时可以通过。
    :param _raster_path: 待重分类的栅格路径
    :param _raster_output_path: 输出栅格的路径
    :param _classify_list: 重分类列表，注意，必须以0为第一个值。eg:[0, 5, 7, 10, 13, 18, 26, 40] 0在输出影像中为nodata，为了使等级从1开始
    :param kwargs: 传入字典列表：{'start', 'end', 'space'} 用于生成等距离间隔。
    :return: None
    """
    # _classify_list优先
    # eg:[5,10,15,20]
    print(''.center(30, '*'))
    print('正在执行重分类'.center(30, ' '))
    classify_list = None
    if _classify_list:
        print('使用给定区间重分类.')
        print(f'分类间隔为:{_classify_list}, 长度为:{len(_classify_list)}')
        classify_list = _classify_list
    elif kwargs:
        print('使用range重分类.')
        classify_list = np.arange(kwargs['start'], kwargs['end'], kwargs['space'])
        print(f'分类间隔为:{classify_list}, 长度为:{len(classify_list)}')
    else:
        print('ERROR：未传入间隔.')
    raster_rr = RR.ReadRaster(_raster_path)
    raster_data = raster_rr.ReadRasterFile()
    print(f'栅格极值为:{raster_rr.pixel_min, raster_rr.pixel_max}')
    print(f'栅格行列为:{raster_rr.raster_ds_y_size, raster_rr.raster_ds_x_size}')
    result_data = np.zeros((raster_rr.raster_ds_y_size, raster_rr.raster_ds_x_size))
    for i in range(raster_rr.raster_ds_y_size):
        for j in range(raster_rr.raster_ds_x_size):
            if raster_data[i][j]:
                level = np.searchsorted(classify_list, raster_data[i][j])
                result_data[i][j] = level
            else:
                continue
    raster_rr.WriteRasterFile(result_data, _raster_output_path, _nodata=0)
    return None


if __name__ == '__main__':
    # # input_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_BaseDEM\NASA_DEM\NASA_DEM.tif'
    # # output_raster_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\NASA_Reclassify_200'
    # # raster_rr = RR.ReadRaster(input_raster_path)
    # # raster_data = raster_rr.ReadRasterFile()
    # # bins_data = RasterReclassify(raster_data, 5400, 6150, 200)
    # # raster_rr.WriteRasterFile(bins_data, output_raster_path)
    # slope_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\Slope_Mask.tif"
    # undulation_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\Undulation_Mask.tif"
    # output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production'
    # output_name = os.path.splitext(os.path.split(undulation_path)[1])[0]
    # output_path = os.path.join(output_folder, f'Reclassify_{output_name}.tif')
    # # RasterReclassify(slope_path, output_path, _classify_list=[0, 3.37, 5.12, 7.12, 9.7, 13.33, 18.96, 27.44])
    # RasterReclassify(undulation_path, output_path, _classify_list=[0, 5, 7, 10, 13, 18, 26, 40])

    # ----
    srtm_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\4_BaseSRTMDEM'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions\Reclassify\Reclassify100'
    path_list, path_filename = PGF.PathGetFiles(srtm_folder, '.tif')
    for index, item in enumerate(path_list):
        RasterReclassify(item, os.path.join(output_folder, path_filename[index] + '_Reclassify100.tif'),
                         _classify_list=[0, 5400, 5500, 5600, 5700, 5800, 5900, 6000, 6100])
