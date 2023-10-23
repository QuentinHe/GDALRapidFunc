# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/16 11:25
# @Author : Hexk
# @Descript : 过滤箱线图中的异常值点，并输出成新的shp文件.
import shutil

import numpy as np
from osgeo import gdal, ogr, osr
import os
import DataAnalysis.Drawing as Drawing
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ShapeFilterOutliers(_input_path, _output_path, _x_df_field, _y_df_field):
    print('正在执行函数ShapeFilterOutliers,去除箱线图中的异常值...')
    input_rsdf = RSDF.ReadPoint2DataFrame(_input_path)
    input_df = input_rsdf.ReadShapeFile()
    boxplot_data_dict = dict()
    for i in np.arange(1, max(input_df[_x_df_field]) + 1):
        #     bin_50_dict[i] = []
        boxplot_data_dict[i] = []
    for index, item in enumerate(input_df[_x_df_field]):
        boxplot_data_dict[item].append(input_df[_y_df_field][index])
    # 绘制箱线图
    print('正在绘制箱线图...')
    boxplot = Drawing.DrawingBoxs(boxplot_data_dict.values(), boxplot_data_dict.keys(), _x_df_field, _y_df_field,
                                  _title=_x_df_field)
    boxs_num, boxs_max, boxs_min = Drawing.DrawingBoxsFilters(boxplot)
    print(f'箱子数量为:{boxs_num}.')
    for i in np.arange(int(boxs_num)):
        print(f'箱子{i + 1} --- Max:{boxs_max[i]}; Min:{boxs_min[i]}')
    # 读取shp文件
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")

    output_name = os.path.splitext(os.path.split(_output_path)[-1])[0]
    if not os.path.exists(_output_path):
        os.makedirs(_output_path)
        print('不存在ShapeFilterOutliers处理后的文件，以创建文件夹...')
    else:
        shutil.rmtree(_output_path)
        print('ShapeFilterOutliers处理后的文件已存在，正在删除...')

    driver = ogr.GetDriverByName('ESRI ShapeFile')
    src_ds = ogr.Open(_input_path)
    src_layer = src_ds.GetLayer()
    ref_srs = src_layer.GetSpatialRef()
    geom_tpye = src_layer.GetGeomType()

    output_ds = driver.CreateDataSource(_output_path)
    output_layer = output_ds.CreateLayer(output_name, ref_srs, geom_tpye)
    temp_feature = src_layer.GetFeature(0)
    src_layer.ResetReading()
    print(f'源Feature个数为:{src_layer.GetFeatureCount()}')

    print('正在为Feature创建原有字段...')
    for n in range(temp_feature.GetFieldCount()):
        output_field = ogr.FieldDefn(input_rsdf.feature_columns[n], temp_feature.GetFieldType(n))
        output_field.SetWidth(50)
        output_field.SetPrecision(8)
        output_layer.CreateField(output_field)

    for num in np.arange(src_layer.GetFeatureCount()):
        feature = src_layer.GetFeature(num)
        filter_value = feature.GetFieldAsDouble(_y_df_field)
        filter_level = feature.GetFieldAsInteger(_x_df_field)
        if boxs_min[filter_level - 1] <= filter_value <= boxs_max[filter_level - 1]:
            output_layer.CreateFeature(feature)
            output_feature = output_layer.GetFeature(output_layer.GetFeatureCount() - 1)
            for n in range(temp_feature.GetFieldCount()):
                output_feature.SetField(input_rsdf.feature_columns[n], feature.GetField(n))
            output_layer.SetFeature(output_feature)
        # else:
        #     print(f'{feature.GetFieldAsDouble("Segment_ID")}')

    print(f'输出数据集长度为:{output_layer.GetFeatureCount()};'
          f'原数据集长度为:{src_layer.GetFeatureCount()};'
          f'过滤数量:{src_layer.GetFeatureCount() - output_layer.GetFeatureCount()};')
    src_ds.Release()
    output_ds.Release()
    return None


if __name__ == '__main__':
    # input_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20230916\1_FilterOutliers\0_AddReduceElevation\SRTM_2019\SRTM_2019.shp'
    # output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20230916\1_FilterOutliers\1_FilterOutliers\SRTM_2019_Bin50'
    # ShapeFilterOutliers(input_path, output_path, 'Bin_50', 'Delta_Ele')
    input_folder_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\9_AddDelta_EleField'
    output_folder_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\10_FilterOutliersData'
    # 遍历指定文件夹获取所有shp文件
    shp_path_list = []
    shp_files_path_list = []
    loop_fields = ['Bin_50', 'Bin_100', 'Bin_150', 'Bin_200']
    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            if os.path.splitext(file)[1] == '.shp':
                shp_path_list.append(os.path.join(root, file))
                shp_files_path_list.append(os.path.splitext(file)[0])
    for index, item in enumerate(shp_path_list):
        for bins in loop_fields:
            ShapeFilterOutliers(item, os.path.join(output_folder_path, shp_files_path_list[index] + '_' + bins), bins,
                                'Delta_Ele')
            print(f'{os.path.join(output_folder_path, shp_files_path_list[index] + "_" + bins)}执行完毕.')
