# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/6 19:45
# @Author : Hexk
# 重投影shape文件

from osgeo import ogr, osr, gdal
import os
os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

def ShapeReprojection(_input_path, _output_path, _other_projection_file_path):
    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF8")

    output_name = os.path.splitext(os.path.split(_output_path)[-1])[0]

    if not os.path.exists(os.path.join(_output_path, output_name)):
        os.makedirs(os.path.join(_output_path, output_name))
        print('不存在Interaction处理后的文件...')
    else:
        os.remove(os.path.join(_output_path, output_name))
        print('Interaction处理后的文件已存在，正在删除...')

    driver = ogr.GetDriverByName('ESRI ShapeFile')
    reproj_ds = ogr.Open(_input_path)
    reproj_layer = reproj_ds.GetLayer()
    geom_tpye = reproj_layer.GetGeomType()

    src_proj_ds = ogr.Open(_other_projection_file_path)
    sr_proj_layer = src_proj_ds.GetLayer()
    ref_srs = sr_proj_layer.GetSpatialRef()

    output_ds = driver.CreateDataSource(os.path.join(_output_path, output_name))
    output_layer = output_ds.CreateLayer(output_name, ref_srs, geom_tpye)

    def_feature = output_layer.GetLayerDefn()

    # feature = reproj_layer.GetFeature(0)
    # feature_geom = feature.GetGeometryRef()
    # help(feature_geom.Transform)

    # 将每个feature都复制到out_Layer
    for feature in reproj_layer:
        geom = feature.GetGeometryRef()
        geom_wkt = geom.ExportToWkt()
        lon = geom_wkt.split(' ')[1][1:]
        lat = geom_wkt.split(' ')[2][:-1]

        prosrs = osr.SpatialReference()
        prosrs.ImportFromEPSG(32646)
        geosrs = prosrs.CloneGeogCS()
        ct = osr.CoordinateTransformation(geosrs, prosrs)
        coords = ct.TransformPoint(float(lat), float(lon))

        out_feature = ogr.Feature(def_feature)
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(coords[0], coords[1], coords[2])
        out_feature.SetGeometry(geom)
        output_layer.CreateFeature(out_feature)

    # 刷新缓存
    output_ds.FlushCache()
    reproj_ds.Release()
    output_ds.Destroy()
    src_proj_ds.Destroy()
    print('重投影完成.')


if __name__ == '__main__':
    input_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\4_Shape_Data\ATL06_Merge\2019\2019.shp'
    output_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\ICESat2\5_ATL06_Reprojection'
    src_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\3_Landsat8_RGI_FourYear\3_Landsat8_RGI_2020.shp'
    ShapeReprojection(input_path, output_path, src_path)
