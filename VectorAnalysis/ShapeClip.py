# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/5 14:20
# @Author : Hexk
# 裁剪矢量文件

import os
import shutil
import PathOperation.PathGetFiles as PGFiles
from osgeo import ogr, gdal

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ShapeClip(input_path, mask_path, output_path):
    """
    矢量裁剪
    :param input_path: 要裁剪的矢量文件
    :param mask_path: 掩膜矢量文件
    :param output_path: 裁剪后的矢量文件保存目录
    :return:
    """
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")
    driver = ogr.GetDriverByName('ESRI SHAPEFILE')
    # 载入要裁剪的矢量文件
    input_ds = ogr.Open(input_path)
    input_layer = input_ds.GetLayer()
    ref_srs = input_layer.GetSpatialRef()
    geom_type = input_layer.GetGeomType()
    # 载入掩膜矢量文件
    mask_ds = ogr.Open(mask_path)
    mask_layer = mask_ds.GetLayer()
    mask_srs = mask_layer.GetSpatialRef()
    output_name = os.path.splitext(os.path.split(output_path)[-1])[0]
    # 生成裁剪后的矢量文件
    if not os.path.exists(output_path):
        print('不存在裁剪后的文件...')
    else:
        shutil.rmtree(output_path)
        print('裁剪后的文件已存在，正在删除...')
    os.makedirs(output_path)
    output_ds = driver.CreateDataSource(output_path)
    output_layer = output_ds.CreateLayer(output_name, ref_srs, geom_type)
    prog_func = gdal.TermProgress_nocb
    input_layer.Clip(mask_layer, output_layer, callback=prog_func)
    output_ds.Destroy()
    input_ds.Destroy()
    mask_ds.Release()
    print('文件裁剪完毕')


def ShapeUpdate(input_path_1, input_path_2, output_path):
    """
    矢量裁剪
    :param input_path_1:
    :param input_path_2:
    :param output_path:
    :return:
    """
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")
    driver = ogr.GetDriverByName('ESRI ShapeFile')

    update_ds = ogr.Open(input_path_1)
    update_layer = update_ds.GetLayer()
    ref_srs = update_layer.GetSpatialRef()

    update2_ds = ogr.Open(input_path_2)
    update2_layer = update2_ds.GetLayer()

    output_name = os.path.splitext(os.path.split(output_path)[-1])[0]

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print('不存在合并后的文件...')
    else:
        os.remove(output_path)
        print('合并后的文件已存在，正在删除...')

    output_ds = driver.CreateDataSource(os.path.join(output_path, f'Update_{output_name}.shp'))
    output_layer = output_ds.CreateLayer(output_name, ref_srs, geom_type=ogr.wkbPolygon)

    prog_func = gdal.TermProgress_nocb

    update_layer.Update(update2_layer, output_layer, callback=prog_func)
    output_ds.Destroy()
    update_ds.Destroy()
    update2_ds.Release()
    print('文件合并完毕')


def ShapeIntersection(input_path_1, input_path_2, output_path):
    """
    保留相交矢量
    :param input_path_1:
    :param input_path_2:
    :param output_path:
    :return:
    """
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")
    driver = ogr.GetDriverByName('ESRI ShapeFile')

    intersection_ds = ogr.Open(input_path_1)
    intersection_layer = intersection_ds.GetLayer()
    ref_srs = intersection_layer.GetSpatialRef()
    geom_tpye = intersection_layer.GetGeomType()

    intersection2_ds = ogr.Open(input_path_2)
    intersection2_layer = intersection2_ds.GetLayer()

    output_name = os.path.splitext(os.path.split(output_path)[-1])[0]

    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print('不存在Interaction处理后的文件...')
    else:
        os.remove(output_path)
        print('Interaction处理后的文件已存在，正在删除...')

    output_ds = driver.CreateDataSource(os.path.join(output_path, f'Interaction_{output_name}.shp'))
    output_layer = output_ds.CreateLayer(output_name, ref_srs, geom_type=geom_tpye)

    prog_func = gdal.TermProgress_nocb

    intersection_layer.Intersection(intersection2_layer, output_layer, callback=prog_func)
    output_ds.Destroy()
    intersection_ds.Destroy()
    intersection2_ds.Release()
    print('文件合并完毕')


if __name__ == '__main__':
    # union1 = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\2_Landsat8_2020_NDSI_Clip\2_Landsat8_2020_NDSI_Clip.shp'
    # union2 = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\2_Landsat8_2022_NDSI_Clip_Update_FilterPitch\Update_2_Landsat8_2022_NDSI_Clip_Update_ClearPitch.shp'
    # # union2 = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\2_Landsat8_2020_NDSI_Clip\2_Landsat8_2020_NDSI_Clip.shp'
    # _output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\2_Landsat8_2022_NDSI_Clip_Update_FilterPitch_Update'
    # ShapeUpdate(union1, union2, _output_folder)

    input_file = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\6_RGI_Point_Data\2020_proj.shp"
    mask_file = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\0_BaseRegion\1_GlaciersRegion\1_GlaciersRegion.shp"
    output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\6_RGI_Point_Data\2020'
    ShapeClip(input_file, mask_file, output_path)
