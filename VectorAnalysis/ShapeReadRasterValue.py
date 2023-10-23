# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/11 10:41
# @Author : Hexk
# @Descript : 用于读取Point点覆盖在Raster上的值，并将值写入DF中，输出成shp
#               不能用DF来输出，坐标系就不是空间直角坐标系了。
#               这个函数使用不能通用，需要对函数内部进行修改。
#               尤其是修改其中对输入字段格式的信息。 OFT.REAL等 若是INT则要用int
import shutil

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ReadRasterValueToShapeField(_input_shape_path, _input_raster_path, _field_name, _output_shape_folder, _output_shape_name, **kwargs):
    print(''.center(30, '*'))
    output_shape_path = os.path.join(_output_shape_folder, _output_shape_name)
    if not os.path.exists(output_shape_path):
        print('不存在ReadRasterValueToShapeField处理后的文件...')
    else:
        shutil.rmtree(output_shape_path)
        print('ReadRasterValueToShapeField处理后的文件已存在，正在删除...')
    os.makedirs(output_shape_path)
    # 读取矢量DataFrame
    input_shape_rsdf = RSDF.ReadPoint2DataFrame(_input_shape_path)
    input_shape_df = input_shape_rsdf.ReadShapeFile()
    # 读取栅格Raster
    input_raster_rr = RR.ReadRaster(_input_raster_path)
    input_raster_data = input_raster_rr.ReadRasterFile()
    # 读取栅格对应点的值
    point_row, point_column = input_shape_rsdf.PointMatchRasterRowColumn(input_raster_rr.raster_ds_geotrans)
    print(f'检验获取行列点是否正常:{point_row[0], point_column[0]}')
    raster_point_value = RR.SearchRasterRowColumnData(point_row, point_column, raster_ds_data=input_raster_data)
    # 解码**kwargs
    kwargs_value_dict = dict()
    if len(kwargs) != 0:
        # key 表示字段名 field， value表示输入的文件路径
        for key, value in kwargs.items():
            kwargs_raster_rr = RR.ReadRaster(value)
            kwargs_raster_data = kwargs_raster_rr.ReadRasterFile()
            kwargs_raster_point_value = RR.SearchRasterRowColumnData(point_row, point_column, raster_ds_data=kwargs_raster_data)
            kwargs_value_dict[key] = kwargs_raster_point_value
    else:
        print(f'kwargs未输入')

    driver = ogr.GetDriverByName('ESRI ShapeFile')
    src_ds = ogr.Open(_input_shape_path)
    src_layer = src_ds.GetLayer()
    ref_srs = src_layer.GetSpatialRef()
    geom_tpye = src_layer.GetGeomType()
    output_ds = driver.CreateDataSource(output_shape_path)
    output_layer = output_ds.CreateLayer(_output_shape_name, ref_srs, geom_tpye)

    temp_feature = src_layer.GetFeature(0)
    print('正在为Feature创建原有字段...')
    for n in range(temp_feature.GetFieldCount()):
        output_field = ogr.FieldDefn(input_shape_rsdf.feature_columns[n], temp_feature.GetFieldType(n))
        output_field.SetWidth(50)
        output_field.SetPrecision(8)
        output_layer.CreateField(output_field)
    print('正在为Feature创建新的字段...')
    output_feature_field = ogr.FieldDefn(_field_name, ogr.OFTReal)
    output_feature_field.SetWidth(50)
    output_feature_field.SetPrecision(8)
    output_layer.CreateField(output_feature_field)
    # 创建**kwargs中的字段
    if kwargs_value_dict:
        for key, value in kwargs_value_dict.items():
            output_feature_field = ogr.FieldDefn(key, ogr.OFTReal)
            output_feature_field.SetWidth(50)
            output_feature_field.SetPrecision(8)
            output_layer.CreateField(output_feature_field)
    else:
        print(f'**kwargs为空.')

    print('正在写入字段信息...')
    for i in range(src_layer.GetFeatureCount()):
        feature = src_layer.GetFeature(i)
        output_layer.CreateFeature(feature)
        output_feature = output_layer.GetFeature(i)
        for n in range(temp_feature.GetFieldCount()):
            output_feature.SetField(input_shape_rsdf.feature_columns[n], feature.GetField(n))
            output_feature.SetField(_field_name, float(raster_point_value[i]))
            if kwargs_value_dict:
                for key, value in kwargs_value_dict.items():
                    output_feature.SetField(key, float(value[i]))
            output_layer.SetFeature(output_feature)
    print(f'写入完成.\n'
              f'原数据集长度为{src_layer.GetFeatureCount()},字段数量为:{src_layer.GetFeature(0).GetFieldCount()};\n'
              f'现数据集长度为{output_layer.GetFeatureCount()},字段数量为:{output_layer.GetFeature(0).GetFieldCount()};')
    src_ds.Release()
    output_ds.Release()
    print(''.center(30, '*'))
    return None


if __name__ == '__main__':
    srtm_dem_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_BaseDEM\SRTM_DEM\SRTM_DEM.tif'
    srtm_slope_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\1_DEM_Slope\SRTM_DEM\1_SRTM_Slope.tif"
    srtm_aspect_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\1_DEM_Aspect\SRTM_Aspect_Level\SRTM_Aspect_Level.tif"
    srtm_undulation_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\3_DEM_Undulation\SRTM\3_SRTM_Undulation.tif"
    srtm_projx_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\4_DEM_ProjCoords\ProjX\ProjX.tif"
    srtm_projy_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\4_DEM_ProjCoords\ProjY\ProjY.tif"
    srtm_bin50_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\SRTM_Reclassify_50\SRTM_Reclassify_50.tif"
    srtm_bin100_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\SRTM_Reclassify_100\SRTM_Reclassify_100.tif"
    srtm_bin150_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\SRTM_Reclassify_150\SRTM_Reclassify_150.tif"
    srtm_bin200_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\SRTM_Reclassify_200\SRTM_Reclassify_200.tif"
    nasa_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_BaseDEM\NASA_DEM\NASA_DEM.tif"
    nasa_slope_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\1_DEM_Slope\NASA_DEM\1_NASA_Slope.tif"
    nasa_aspect_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\1_DEM_Aspect\NASA_Aspect_Level\NASA_Aspect_Level.tif"
    nasa_undulation_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\3_DEM_Undulation\NASA\3_NASA_Undulation.tif"
    nasa_projx_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\4_DEM_ProjCoords\ProjX\ProjX.tif"
    nasa_projy_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\4_DEM_ProjCoords\ProjY\ProjY.tif"
    nasa_bin50_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\NASA_Reclassify_50\NASA_Reclassify_50.tif"
    nasa_bin100_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\NASA_Reclassify_100\NASA_Reclassify_100.tif"
    nasa_bin150_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\NASA_Reclassify_150\NASA_Reclassify_150.tif"
    nasa_bin200_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\NASA_Reclassify_200\NASA_Reclassify_200.tif"

    output_shape_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\8_RasterFieldData'
    input_shape_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\7_Remove_Slope_Data'
    shape_file_list, shape_name_list = PGFiles.PathGetFiles(input_shape_folder, '.shp')
    nasa_shape_list = []
    srtm_shape_list = []
    for index, item in enumerate(shape_name_list):
        if item.split('_')[0] == 'NASA':
            nasa_shape_list.append(shape_file_list[index])
        else:
            srtm_shape_list.append(shape_file_list[index])

    for i in nasa_shape_list:
        filename = os.path.splitext(os.path.split(i)[1])[0]
        nasa_field_dict = dict(
            Proj_X=nasa_projx_path,
            Proj_Y=nasa_projy_path,
            Aspect=nasa_aspect_path,
            Slope=nasa_slope_path,
            Bin_50=nasa_bin50_path,
            Bin_100=nasa_bin100_path,
            Bin_150=nasa_bin150_path,
            Bin_200=nasa_bin200_path,
            Undulation=nasa_undulation_path,
        )
        ReadRasterValueToShapeField(i, nasa_dem_path, 'Elevation', output_shape_folder, filename, **nasa_field_dict)
    for i in srtm_shape_list:
        filename = os.path.splitext(os.path.split(i)[1])[0]
        srtm_field_dict = dict(
            Proj_X=srtm_projx_path,
            Proj_Y=srtm_projy_path,
            Aspect=srtm_aspect_path,
            Slope=srtm_slope_path,
            Bin_50=srtm_bin50_path,
            Bin_100=srtm_bin100_path,
            Bin_150=srtm_bin150_path,
            Bin_200=srtm_bin200_path,
            Undulation=srtm_undulation_path,
        )
        ReadRasterValueToShapeField(i, srtm_dem_path, 'Elevation', output_shape_folder, filename, **srtm_field_dict)
