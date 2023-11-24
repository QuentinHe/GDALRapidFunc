# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/13 下午3:15
# @Author : Hexk
# @Descript : 从栅格文件中读取像元值，并写入Point中。

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


def ReadRasterValueToShapeField(_input_shape_path, _output_shape_folder,
                                _output_shape_name, **kwargs):
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
    # # 读取栅格Raster
    # input_raster_rr = RR.ReadRaster(_input_raster_path)
    # input_raster_data = input_raster_rr.ReadRasterFile()
    # # 读取栅格对应点的值
    # point_row, point_column = input_shape_rsdf.PointMatchRasterRowColumn(input_raster_rr.raster_ds_geotrans)
    # print(f'检验获取行列点是否正常:{point_row[0], point_column[0]}')
    # raster_point_value = RR.SearchRasterRowColumnData(point_row, point_column, raster_ds_data=input_raster_data)
    # 解码**kwargs
    kwargs_value_dict = dict()
    if len(kwargs) != 0:
        # key 表示字段名 field， value表示输入的文件路径
        for key, value in kwargs.items():
            kwargs_raster_rr = RR.ReadRaster(value)
            kwargs_raster_data = kwargs_raster_rr.ReadRasterFile()
            point_row, point_column = input_shape_rsdf.PointMatchRasterRowColumn(kwargs_raster_rr.raster_ds_geotrans)
            kwargs_raster_point_value = RR.SearchRasterRowColumnData(point_row, point_column,
                                                                     raster_ds_data=kwargs_raster_data)
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
            # output_feature.SetField(_field_name, float(raster_point_value[i]))
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
    srtm_dem_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\4_BaseSRTMDEM'
    aspect_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions\Aspect'
    slope_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions\Slope'
    undulation_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions\Undulation'
    reclassify50_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions\Reclassify\Reclassify50'
    reclassify100_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions\Reclassify\Reclassify100'
    reclassify150_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions\Reclassify\Reclassify150'
    reclassify200_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions\Reclassify\Reclassify200'

    output_shape_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\8_Raster_Field_Point_Data'
    input_shape_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\7_Remove_Slope_Data'

    shape_file_list, shape_name_list = PGFiles.PathGetFiles(input_shape_folder, '.shp')
    srtm_dem_list, srtm_dem_name_list = PGFiles.PathGetFiles(srtm_dem_folder, '.tif')
    aspect_list, aspect_name_list = PGFiles.PathGetFiles(aspect_folder, '.tif')
    slope_list, slope_name_list = PGFiles.PathGetFiles(slope_folder, '.tif')
    undulation_list, undulation_name_list = PGFiles.PathGetFiles(undulation_folder, '.tif')
    reclassify50_list, reclassify50_name_list = PGFiles.PathGetFiles(reclassify50_folder, '.tif')
    reclassify100_list, reclassify100_name_list = PGFiles.PathGetFiles(reclassify100_folder, '.tif')
    reclassify150_list, reclassify150_name_list = PGFiles.PathGetFiles(reclassify150_folder, '.tif')
    reclassify200_list, reclassify200_name_list = PGFiles.PathGetFiles(reclassify200_folder, '.tif')
    srtm_projx_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\4_DEM_ProjCoords\ProjX\ProjX.tif"
    srtm_projy_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\4_DEM_ProjCoords\ProjY\ProjY.tif"

    type_list = ['Minus5', 'Minus10', 'Plus5', 'Plus10', 'Random5', 'Random10']
    abbreviative_type_list = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10']
    point_field_dict = dict(
        Proj_X=srtm_projx_path,
        Proj_Y=srtm_projy_path,
    )
    for index, item in enumerate(type_list):
        srtm_item = None
        asp_item = None
        slope_item = None
        undulation_item = None
        reclassify50_item = None
        reclassify100_item = None
        reclassify150_item = None
        reclassify200_item = None
        for name_index, name_item in enumerate(srtm_dem_name_list):
            if name_item.split('_')[1] == item:
                srtm_item = srtm_dem_list[name_index]
                print(srtm_item)
                break
            else:
                print(f'未查询到{item}的srtm_dem_name')
        for name_index, name_item in enumerate(aspect_name_list):
            if name_item.split('_')[1] == item:
                asp_item = aspect_list[name_index]
                print(asp_item)
                break
            else:
                print(f'未查询到{item}的aspect_name')
        for name_index, name_item in enumerate(slope_name_list):
            if name_item.split('_')[1] == item:
                slope_item = slope_list[name_index]
                print(slope_item)
                break
            else:
                print(f'未查询到{item}的slope_name')
        for name_index, name_item in enumerate(undulation_name_list):
            if name_item.split('_')[1] == item:
                undulation_item = undulation_list[name_index]
                print(undulation_item)
                break
            else:
                print(f'未查询到{item}的undulation_name')
        for name_index, name_item in enumerate(reclassify50_name_list):
            if name_item.split('_')[1] == item:
                reclassify50_item = reclassify50_list[name_index]
                print(reclassify50_item)
                break
            else:
                print(f'未查询到{item}的reclassify50_name')
        for name_index, name_item in enumerate(reclassify100_name_list):
            if name_item.split('_')[1] == item:
                reclassify100_item = reclassify100_list[name_index]
                print(reclassify100_item)
                break
            else:
                print(f'未查询到{item}的reclassify100_name')
        for name_index, name_item in enumerate(reclassify150_name_list):
            if name_item.split('_')[1] == item:
                reclassify150_item = reclassify150_list[name_index]
                print(reclassify150_item)
                break
            else:
                print(f'未查询到{item}的reclassify150_name')
        for name_index, name_item in enumerate(reclassify200_name_list):
            if name_item.split('_')[1] == item:
                reclassify200_item = reclassify200_list[name_index]
                print(reclassify200_item)
                break
            else:
                print(f'未查询到{item}的reclassify200_name')
        temp_dict = {
            f'DEM_{abbreviative_type_list[index]}': srtm_item,
            f'Asp_{abbreviative_type_list[index]}': asp_item,
            f'Slp_{abbreviative_type_list[index]}': slope_item,
            f'Und_{abbreviative_type_list[index]}': undulation_item,
            f'B50_{abbreviative_type_list[index]}': reclassify50_item,
            f'B100_{abbreviative_type_list[index]}': reclassify100_item,
            f'B150_{abbreviative_type_list[index]}': reclassify150_item,
            f'B200_{abbreviative_type_list[index]}': reclassify200_item,
        }
        point_field_dict = dict(**point_field_dict, **temp_dict)
    print(point_field_dict)
    for index, item in enumerate(shape_file_list):
        output_shape_name = shape_name_list[index] + '_TestSupplement'
        ReadRasterValueToShapeField(item, output_shape_folder, output_shape_name, **point_field_dict)
