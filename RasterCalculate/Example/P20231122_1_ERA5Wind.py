# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/22 10:19
# @Author : Hexk
# @Descript :

import os
import matplotlib
import numpy as np
from datetime import datetime
from datetime import timedelta
import netCDF4 as nc
import glob
import json
import matplotlib.pyplot as plt
from osgeo import gdal
import pandas as pd
from scipy import interpolate
from scipy import ndimage
from nansat import Nansat
import common_lib as clib

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':

    file_path = R"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231122_1_ERA5Wind\ERA5_Wind_00-22.nc"

    ERA5_BASE_TIME = datetime(year=1900, month=1, day=1)

    # 提取NC文件中的相应数据
    wind_data = nc.Dataset(file_path)

    lon_arr = wind_data.variables['longitude'][:]
    lat_arr = wind_data.variables['latitude'][:]
    wind_time = wind_data.variables['time'][:]
    u10 = wind_data.variables['u10'][:]
    v10 = wind_data.variables['v10'][:]
    si10 = wind_data.variables['si10'][:]

    # 将经纬度转为grid格式，并用flatten()把它从二维变为一维
    lon_grid, lat_grid = np.meshgrid(lon_arr, lat_arr)
    lon_grid = lon_grid.flatten()
    lat_grid = lat_grid.flatten()

    # 读取研究区域的经纬度文件"/mnt/g/aaa/gate_shape/MIZ_lon_lat_arr.csv"
    # miz_extent_data = np.loadtxt("/mnt/g/aaa/gate_shape/MIZ_lon_lat_arr.csv", skiprows=1, delimiter=",")
    # lon_arr_miz = miz_extent_data[:, 0]
    # lat_arr_miz = miz_extent_data[:, 1]
    lon_arr_miz = [90, 91, 92]
    lat_arr_miz = [33, 34]

    # 循环计算出在NC文件上，离研究区域的每个点最近的经纬度的index，就可以利用index索引研究区域的数据。
    for i in range(len(lon_arr_miz)):
        lon = lon_arr_miz[i]
        lat = lat_arr_miz[i]
        distance = (lon_grid - lon) ** 2 + (lat_grid - lat) ** 2
        index = np.argmin(distance)
        pass

    sub_u10 = []
    sub_v10 = []
    sub_si10 = []
    monthly_time = []
    for i in range(len(wind_time)):
        key = ERA5_BASE_TIME + timedelta(hours=int(wind_time[i]))
        monthly_time.append(key)
        sub_u10.append(u10[i].flatten()[index])
        sub_v10.append(v10[i].flatten()[index])
        sub_si10.append(si10[i].flatten()[index])

    sub_lon, sub_lat = lon_grid[index], lat_grid[index]

    # 下面开始算风速方向
    deg = 180.0 / np.pi
    monthly_time_p = []
    sub_si10_p = []
    wdir = []

    # 用循环将每年12月的风速一个个输出到sub_si10_p[]，并将12月平均风向一个个加到wdir[]
    for i, t in enumerate(monthly_time):
        if t.month == 12:
            monthly_time_p.append(t)
            sub_si10_p.append(np.nanmean(sub_si10[i]))
            # 利用u/v计算风速方向
            wdir.append(180.0 + np.arctan2(np.nanmean(sub_u10[i]), np.nanmean(sub_v10[i])) * deg)

    # 将结果输出为csv
    dataframe = pd.DataFrame({"time": monthly_time_p, "wspd": sub_si10_p, "wdir": wdir})
    dataframe.to_csv(f"wind_0220.csv", index=False)
