# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/10 10:37
# @Author : Hexk
# @Descript : 随机抽样，读取shp样本点个数，随机选择百分比，并通过ID找到要素进行切分。
import random
import shutil
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadShape2DataFrame as RSDF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ShapeRandomSampling(_input_path, _output_path, _feature_columns, _percent):
    """
    随机采样，分类point样本点
    :param _input_path: 输入的shape文件
    :param _output_path: 输出地址
    :param _feature_columns: 需要输入的属性表field字段list
    :param _percent: 需要输入的百分比，1~99
    :return: None
    """
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")

    if _percent >= 100 or _percent <= 0:
        print(f'RandomSampling的比例不能为{_percent}!')
        return None

    output_name = os.path.splitext(os.path.split(_output_path)[-1])[0]

    if not os.path.exists(_output_path):
        os.makedirs(_output_path)
        print('不存在ShapeRandomSampling处理后的文件，以创建文件夹...')
    else:
        shutil.rmtree(_output_path)
        print('ShapeRandomSampling处理后的文件已存在，正在删除...')

    driver = ogr.GetDriverByName('ESRI ShapeFile')
    src_ds = ogr.Open(_input_path)
    src_layer = src_ds.GetLayer()
    ref_srs = src_layer.GetSpatialRef()
    geom_tpye = src_layer.GetGeomType()
    # 按照percent来创建随机采样后的shape文件
    output_part1_ds = driver.CreateDataSource(_output_path)
    output_part1_name = f'{output_name}_{_percent}'
    output_part1_layer = output_part1_ds.CreateLayer(output_part1_name, ref_srs, geom_tpye)
    output_part2_ds = driver.CreateDataSource(_output_path)
    output_part2_name = f'{output_name}_{100 - _percent}'
    output_part2_layer = output_part2_ds.CreateLayer(output_part2_name, ref_srs, geom_tpye)
    # 为output_layer创建Field，此时8个field字段就写入到output_layer中
    temp_feature = src_layer.GetFeature(0)
    for n in range(temp_feature.GetFieldCount()):
        output_field = ogr.FieldDefn(_feature_columns[n], temp_feature.GetFieldType(n))
        output_field.SetWidth(50)
        output_field.SetPrecision(8)
        output_part1_layer.CreateField(output_field)
        output_part2_layer.CreateField(output_field)
    src_layer.ResetReading()
    print(f'源Feature个数为:{src_layer.GetFeatureCount()}')
    print(f'开始随机分类feature信息...')
    # 生成两列随机序列
    all_sample = list(range(src_layer.GetFeatureCount()))
    main_sample = random.sample(all_sample, int(np.rint(src_layer.GetFeatureCount() * _percent / 100)))
    print(f'全数据集长度为:{len(all_sample)},主数据集长度为:{len(main_sample)},正在分类...')
    for num in range(src_layer.GetFeatureCount()):
        if num in main_sample:
            feature = src_layer.GetFeature(num)
            output_part1_layer.CreateFeature(feature)
            # 为output_layer的feature赋值
            output_feature = output_part1_layer.GetFeature(output_part1_layer.GetFeatureCount() - 1)
            for n in range(temp_feature.GetFieldCount()):
                output_feature.SetField(_feature_columns[n], feature.GetField(n))
            output_part1_layer.SetFeature(output_feature)
        else:
            feature = src_layer.GetFeature(num)
            output_part2_layer.CreateFeature(feature)
            # 为output_layer的feature赋值
            output_feature = output_part2_layer.GetFeature(output_part2_layer.GetFeatureCount() - 1)
            for n in range(temp_feature.GetFieldCount()):
                output_feature.SetField(_feature_columns[n], feature.GetField(n))
            output_part2_layer.SetFeature(output_feature)
    print(
        f'主数据集长度为:{output_part1_layer.GetFeatureCount()},所占百分比为:{output_part1_layer.GetFeatureCount() / src_layer.GetFeatureCount()};\n'
        f'次数据集长度为:{output_part2_layer.GetFeatureCount()},所占百分比为:{output_part2_layer.GetFeatureCount() / src_layer.GetFeatureCount()}')
    src_ds.Release()
    output_part1_ds.Release()
    output_part2_ds.Release()


if __name__ == '__main__':
    input_shape_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\8_All_Raster_DataFrame_Data\5_Elevation\SRTM_2019\SRTM_2019.shp'
    output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\9_RandomSampling_Data\SRTM_2019'
    input_shape_rsdf = RSDF.ReadPoint2DataFrame(input_shape_path)
    input_shape_df = input_shape_rsdf.ReadShapeFile()
    ShapeRandomSampling(input_shape_path, output_path, input_shape_rsdf.feature_columns, 70)
