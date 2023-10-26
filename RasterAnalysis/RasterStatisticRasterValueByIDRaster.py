# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/18 10:49
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR
from ReadRasterAndShape.ReadShape2DataFrame import ReadShape2DataFrame

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def RasterStatisticRasterValueByIDRaster(_src_raster_path, _id_raster_path, _output_csv_path=None):
    # 读取两个栅格文件
    print(''.center(30, '*'))
    print(f'正在执行函数RasterStatisticRasterValueByIDRaster...')
    src_rr = RR.ReadRaster(_src_raster_path)
    src_raster_data = src_rr.ReadRasterFile()
    id_rr = RR.ReadRaster(_id_raster_path)
    id_raster_data = id_rr.ReadRasterFile()
    id_raster_max = id_rr.pixel_max
    id_max = np.max(id_raster_data)
    id_raster_min = id_rr.pixel_min
    id_min = np.min(id_raster_data)
    # 这里存在问题，band统计后的结果与np统计的不符合
    # print(id_raster_max, id_raster_min)
    # print(id_max, id_min)
    id_raster_nodata = id_rr.nodata
    # 统计，写入dict
    id_dict = dict()
    print(f'正在统计...')
    for i in np.arange(id_raster_min, np.max(id_raster_data) + 1):
        i = int(i)
        id_dict[i] = []
    for y in range(id_rr.raster_ds_y_size):
        for x in range(id_rr.raster_ds_x_size):
            raster_id = id_raster_data[y][x]
            if raster_id != id_raster_nodata:
                value = src_raster_data[y][x]
                id_dict[raster_id].append(value)
            else:
                continue
    # 变成统计结果
    sum_list = []
    mean_list = []
    pixel_num_list = []
    for key, value in id_dict.items():
        sum_list.append(np.sum(value))
        mean_list.append(np.mean(value))
        pixel_num_list.append(len(value))
    csv_dict = dict(
        ID=id_dict.keys(),
        Sum=sum_list,
        Mean=mean_list,
        PixelNums=pixel_num_list,
    )
    _csv_df = pd.DataFrame(csv_dict)
    print(_csv_df)
    if _output_csv_path:
        _csv_df.to_csv(_output_csv_path)
    print(''.center(30, '*'))
    return _csv_df


if __name__ == '__main__':
    # src_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\4_MeanData\SRTM_2019\SRTM_2019.tif"
    src_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Result_20231022\3_GlaciersDepths\DeltaIceDepths.tif"
    # id_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\4_AnalysisRaster\2_Rasterize\Rasterize.tif"
    id_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Result_20231022\3_GlaciersDepths\GLACID.tif"
    output_csv_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Result_20231022\3_GlaciersDepths\DeltaIceDepths.csv'
    csv_df = RasterStatisticRasterValueByIDRaster(src_path, id_path)
    shape_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\0_BaseRegion\2_GlaciersRGIRegion\Tanggula_Region_RGI.shp"
    polygon_rpdf = ReadShape2DataFrame(shape_path)
    polygon_df = polygon_rpdf.ReadShapeFile()
    glacier_name = polygon_df['Name']
    csv_df.insert(loc=1, column='Glaciers_Name', value=glacier_name)
    csv_df.to_csv(output_csv_path)
