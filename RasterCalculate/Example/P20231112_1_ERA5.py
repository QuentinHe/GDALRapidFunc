# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/12 10:13
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import netCDF4 as nc


def write_img(filename, im_proj, im_geotrans, im_data):
    # 判断栅格数据的数据类型
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32
    # 判读数组维数
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape
    # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)
    dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
    dataset.SetProjection(im_proj)  # 写入投影
    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


def nc_totif(input_path, output_path):
    # 读取nc文件
    tep_data = nc.Dataset(input_path)
    # 获取nc文件中对应变量的信息
    lon_data = tep_data.variables["longitude"][:]
    lat_data = tep_data.variables["latitude"][:]
    # 影像的左上角&右下角坐标
    lonmin, latmax, lonmax, latmin = [lon_data.min(), lat_data.max(), lon_data.max(), lat_data.min()]
    # 分辨率计算
    num_lon = len(lon_data)  # 281
    num_lat = len(lat_data)  # 241
    lon_res = (lonmax - lonmin) / (float(num_lon) - 1)
    lat_res = (latmax - latmin) / (float(num_lat) - 1)
    # 定义投影
    proj = osr.SpatialReference()
    proj.ImportFromEPSG(4326)  # WGS84
    proj = proj.ExportToWkt()  # 重点，转成wkt格式
    # print(prj)     字符串
    geotransform = (lonmin, lon_res, 0.0, latmax, 0.0, -lat_res)
    # 获取2m温度
    # t2m = tep_data.variables["t2m"][:]  # (60, 241, 281)
    # t2m_arr = np.asarray(t2m)
    #
    # tp = tep_data.variables['tp'][:]
    # tp_arr = np.asarray(tp)
    u10 = tep_data.variables["u10"][:]  # (60, 241, 281)
    u10_arr = np.asarray(u10)

    v10 = tep_data.variables['v10'][:]
    v10_arr = np.asarray(v10)

    si10 = tep_data.variables['si10'][:]
    si10_arr = np.asarray(si10)
    # 年份
    yearlist = [i for i in range(2000, 2023)]
    for i in range(len(yearlist)):
        year = yearlist[i]
        for j in range(12 * i, 12 * (i + 1)):
            month = (j % 12) + 1
            u10_outputpath = os.path.join(output_path, f'{year}_{month}_u10.tif')
            v10_outputpath = os.path.join(output_path, f'{year}_{month}_v10.tif')
            si10_outputpath = os.path.join(output_path, f'{year}_{month}_si10.tif')
            write_img(u10_outputpath, proj, geotransform, u10_arr[j])
            write_img(v10_outputpath, proj, geotransform, v10_arr[j])
            write_img(si10_outputpath, proj, geotransform, si10_arr[j])


os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    input_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231122_1_ERA5Wind\ERA5_Wind_00-22.nc"
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231122_1_ERA5Wind\20231122_1_WindTif'
    # 读取nc文件，转换为tif文件
    nc_totif(input_path, output_folder)
