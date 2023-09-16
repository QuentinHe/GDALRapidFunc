# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/8/28 9:59
# @Author : Hexk
import shutil

import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os


# 转换DataFrame的列格式
def DataFrameFormatConvert(df, int_field=None, float_field=None, string_field=None):
    """
    转换DataFrame的列格式
    :param string_field:    需要改变为string的DF字段
    :param float_field: 需要改变为float的DF字段
    :param int_field:   需要改变为int的DF字段
    :param df: DataFrame
    :return: DataFrame
    """

    _feature_df = df
    print('-------正在转换DataFrame数据类型------')
    print(f'当前输入对象的数据类型为:\n{_feature_df.dtypes}')
    if int_field is not None:
        # 转化为整数的需要先转化为浮点
        _feature_df[int_field] = _feature_df[int_field].astype('float32')
        _feature_df[int_field] = _feature_df[int_field].astype('uint16')
    if float_field is not None:
        _feature_df[float_field] = _feature_df[float_field].astype('float32')
    if string_field is not None:
        string_field = []
        _feature_df[string_field] = _feature_df[float_field].astype('string')
    print(f'已将数据类型转化为:\n{_feature_df.dtypes}')
    return _feature_df


def AspectConvertLevel(aspect_list):
    """
    将坡向按照八个方向进行分级，0是不可用等级，范围是1~8
    :param aspect_list: DataFrame的feature_df['Aspect']或者其他的list格式
    :return:    转化为等级的list格式
    """
    print('------正在进行坡向转等级------')
    aspect_level_list = []
    for i in aspect_list:
        aspect_level = np.ceil((i - 22.5) / 45) + 1
        if aspect_level > 8 or aspect_level < 1 or np.isnan(aspect_level):
            aspect_level = 0
        elif aspect_level == 9:
            aspect_level = 1
        aspect_level_list.append(aspect_level)
    print(f'共转换坡向数量：{len(aspect_level_list)}')
    return np.array(aspect_level_list)


def DataFrameWriteShape(_feature_df, _output_path, _output_prefix):
    if os.path.exists(os.path.join(_output_path, _output_prefix)):
        os.remove(os.path.join(_output_path, _output_prefix))
    else:
        print(f'在当前输出目录下不存在文件夹.')
    os.makedirs(os.path.join(_output_path, _output_prefix))
    output_filename = f'{_output_prefix}.shp'
    # gdal设置空间参考系
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(4326)
    # 设置驱动格式
    driver = ogr.GetDriverByName('ESRI SHAPEFILE')
    # 新建shp文件
    new_shp_ds = driver.CreateDataSource(os.path.join(_output_path, _output_prefix, output_filename))
    # 新建shp文件中的图层
    layer = new_shp_ds.CreateLayer(output_filename, srs=spatial_ref, geom_type=ogr.wkbPoint)
    filed_names = list(_feature_df)
    # 新建shp文件图层中的字段,csv中所有列为字段名和字段数据
    for item in filed_names:
        # 判断字段类型，并新增字段
        if "int" in str(_feature_df[item].dtypes):
            field_def = ogr.FieldDefn(item, ogr.OFTInteger)
            field_def.SetWidth(100)
            layer.CreateField(field_def)
        elif "float" in str(_feature_df[item].dtypes):
            field_def = ogr.FieldDefn(item, ogr.OFTReal)
            field_def.SetWidth(100)
            field_def.SetPrecision(20)
            layer.CreateField(field_def)
        else:
            field_def = ogr.FieldDefn(item, ogr.OFTString)
            field_def.SetWidth(100)
            layer.CreateField(field_def)
    # 为图层创建feature
    feature_def = layer.GetLayerDefn()
    feature = ogr.Feature(feature_def)
    point = ogr.Geometry(ogr.wkbPoint)
    # 循环写入字段属性
    for i in range(len(_feature_df)):
        for j in range(len(filed_names)):
            if "int" in str(_feature_df[filed_names[j]].dtypes):
                feature.SetField(filed_names[j], int(_feature_df.iloc[i, j]))
            elif "float" in str(_feature_df[filed_names[j]].dtypes):
                feature.SetField(filed_names[j], float(_feature_df.iloc[i, j]))
            else:
                feature.SetField(filed_names[j], str(_feature_df.iloc[i, j]))
        # 设定几何信息，包括经纬度、高程
        point.AddPoint(float(_feature_df.iloc[i]['Longitudes']), float(_feature_df.iloc[i]['Latitudes']),
                       float(_feature_df.iloc[i]['H_Li']))
        # 往要素中写入点
        feature.SetGeometry(point)
        # 往图层中写入要素
        layer.CreateFeature(feature)
    point.Destroy()
    feature.Destroy()
    new_shp_ds.Destroy()
    print(f'文件{output_filename}写入完毕，存储路径为：{os.path.join(_output_path, output_filename)}')


class ReadPoint2DataFrame:
    def __init__(self, input_path):
        self.feature_geom_list = None
        self.input_path = input_path
        self.feature_columns = None

    def ReadShapeFile(self):
        """
        Function:   读取Point Shape文件

        :return:    DataFrame
        """
        gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
        # 属性表字段支持中文
        gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
        # 注册驱动
        ogr.RegisterAll()
        # 新建dataset，打开shp文件
        ds = ogr.Open(self.input_path)
        # 获取dataset的图层个数
        ds.GetLayerCount()
        # 获取第一个图层
        layer = ds.GetLayerByIndex(0)
        # 重置要素读取序列
        layer.ResetReading()
        # 获取当前图层由多少个矢量要素
        feature_num = layer.GetFeatureCount(0)
        print('------正在读取Shape------')
        print(f'当前图层有{feature_num}个要素.')
        # 获取属性表
        feature_define = layer.GetLayerDefn()
        # 获取属性表的字段个数
        feature_define_count = feature_define.GetFieldCount()
        # 存储属性表表头
        feature_columns = []
        feature_columns_types = []
        # 循环输出字段的信息
        for index in range(feature_define_count):
            feature_field = feature_define.GetFieldDefn(index)
            # 获取字段名称，这个部分在DF写入属性的时候有用
            feature_name = feature_field.GetNameRef()
            feature_columns.append(feature_name)
            # 获取字段的数据类型
            feature_columns_types.append(feature_field.GetFieldTypeName(feature_field.GetType()))
            # # 获取字段的宽度
            # feature_field.GetWidth()
            # # 获取字段的小数点精度
            # feature_field.GetPrecision()
        print(f'当前属性表有以下字段:{feature_columns},数据类型为:{feature_columns_types}')
        # 按顺序读取所有要素的属性
        self.feature_columns = feature_columns
        # 新建一个属性字典，用于存储整个矢量的属性表信息, 循环为字典内创建变量
        feature_attribute_dict = dict(((name, []) for name in feature_columns))
        # 创建一个geom list，用于存储点要素的geom数据
        feature_geom_list = []
        # 循环读取每一个要素
        for i in range(feature_num):
            feature = layer.GetFeature(i)
            # 获取点要素的geom
            feature_geom = str(feature.GetGeometryRef())
            feature_geom_x = float(feature_geom.split(' ')[1][1:])
            feature_geom_y = float(feature_geom.split(' ')[2][:-1])
            feature_geom_list.append((feature_geom_x, feature_geom_y))
            # 循环每一个表头，并在dict中添加要素的每一列数据
            for index, item in enumerate(feature_columns):
                if feature_columns_types[index] == 'Real':
                    feature_attribute_dict[item].append(feature.GetFieldAsDouble(item))
                elif feature_columns_types[index] == 'Integer':
                    feature_attribute_dict[item].append(feature.GetFieldAsInteger(item))
                else:
                    feature_attribute_dict[item].append(feature.GetFieldAsString(item))
        self.feature_geom_list = feature_geom_list
        ds.Destroy()
        del ds
        _feature_df = pd.DataFrame(feature_attribute_dict)
        print(f'DataFrame长度为:{len(_feature_df)}')
        return _feature_df

    def PointMatchRasterRowColumn(self, raster_geo_transform):
        """
        通过self.feature_geom_list中的point x y大地坐标来对应找到栅格对应的点位置
        :param raster_geo_transform:
        :return:
        """
        print('------正在计算点要素对应栅格面上的行列位置------')
        raster_origin_x = raster_geo_transform[0]
        raster_origin_y = raster_geo_transform[3]
        pixel_x = raster_geo_transform[1]
        pixel_y = raster_geo_transform[5]

        point_column = []
        point_row = []
        for item in self.feature_geom_list:
            _column = int(np.ceil((item[0] - raster_origin_x) / pixel_x))
            _row = int(np.ceil((item[1] - raster_origin_y) / pixel_y))
            point_column.append(_column)
            point_row.append(_row)
        print(f'当前行列数长度为:{len(point_row), len(point_column)}')
        return point_row, point_column


if __name__ == '__main__':
    atl06_path = r'E:\Glacier_DEM_Register\Tanggula_ICESat2\10_XGBoost_Data\8_ATL06_75.shp'
    ATL06_75 = ReadPoint2DataFrame(atl06_path)
    feature_df = ATL06_75.ReadShapeFile()
    feature_df = DataFrameFormatConvert(feature_df, int_field=['Segment_ID', 'NASA_Level', 'SRTM_Level'],
                                        float_field=['Latitudes', 'Longitudes', 'H_Li', 'DEM_H', 'Delta_H', 'NASADEM',
                                                     'Delta_NASA',
                                                     'SRTMDEM', 'Delta_SRTM'])
    geoTransform = (219686.5887, 29.999489275454838, 0.0, 3766230.5, 0.0, -30.001324679067285)
    row, column = ATL06_75.PointMatchRasterRowColumn(geoTransform)
    print(row[1], column[1])
