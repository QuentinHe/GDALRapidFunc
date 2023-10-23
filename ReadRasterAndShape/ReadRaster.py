# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/8/28 11:16
# @Author : Hexk

import os
import shutil

from osgeo import gdal, osr


def SearchRasterRowColumnData(point_row, point_column, raster_ds_data=None, _raster_ds_path=None):
    """
    根据已知的点在栅格上的行列位置，获取栅格上的信息
    :param _raster_ds_path: raster_ds_data的路径
    :param raster_ds_data:  N行M列的多维矩阵
    :param point_row:   点位的行数组
    :param point_column:    点位的列数组
    :return:    在Raster上查找到对应位置的数据
    """
    if len(point_row) != len(point_column):
        print('Error:点位的行列数不等')
    raster_row_column_data = []
    if _raster_ds_path is not None and raster_ds_data is None:
        raster_rr = ReadRaster(_raster_ds_path)
        raster_data = raster_rr.ReadRasterFile()
        for i in range(len(point_row)):
            raster_row_column_data.append(raster_data[point_row[i]][point_column[i]])
    elif _raster_ds_path is None and raster_ds_data is not None:
        for i in range(len(point_row)):
            raster_row_column_data.append(raster_ds_data[point_row[i]][point_column[i]])
    return raster_row_column_data


class ReadRaster:
    def __init__(self, input_path):
        self.input_path = input_path
        self.raster_ds_proj = None
        self.raster_ds_geotrans = None
        self.raster_ds_y_size = None
        self.raster_ds_x_size = None
        self.nodata = None
        self.pixel_min = None
        self.pixel_max = None
        self.pixel_mean = None
        self.pixel_std = None

    def ReadRasterFile(self):
        """
        读取栅格文件
        :return:    np.array格式的多维数组，未降维，降维需要.shape(-1)
        """
        gdal.AllRegister()
        raster_ds = gdal.Open(self.input_path)
        raster_ds_band = raster_ds.GetRasterBand(1)
        self.raster_ds_x_size = raster_ds.RasterXSize  # 栅格矩阵的列数
        self.raster_ds_y_size = raster_ds.RasterYSize  # 栅格矩阵的行数
        self.raster_ds_geotrans = raster_ds.GetGeoTransform()  # 仿射矩阵，左上角像素的大地坐标和像素分辨率
        self.raster_ds_proj = raster_ds.GetProjection()  # 地图投影信息，字符串表示
        self.nodata = raster_ds_band.GetNoDataValue()   # 栅格中设定的nodata值
        band_stat = raster_ds_band.GetStatistics(True, True)
        self.pixel_min = band_stat[0]   # 栅格最小值，不包含Nodata
        self.pixel_max = band_stat[1]   # 栅格最大值
        self.pixel_mean = band_stat[2]  # 栅格均值
        self.pixel_std = band_stat[3]   # 栅格标准差
        raster_ds_data = raster_ds_band.ReadAsArray()
        return raster_ds_data

    def ReadRasterLatLon(self):
        """
        读取栅格影像上每个像元的经纬度
        ---
        按理说，行列数知道，整个图的经纬度表也知道，可以求一行和一列，之后按照index来查找。
        下面这个方法计算很慢。
        有空重写一下。
        ---
        :return: 纬度和经度的列表
        """
        print('正在读取经纬度信息'.center(20, '-'))
        _pixel_location = []
        prosrs = osr.SpatialReference()
        prosrs.ImportFromWkt(self.raster_ds_proj)
        geosrs = prosrs.CloneGeogCS()
        ct = osr.CoordinateTransformation(prosrs, geosrs)
        for i in range(self.raster_ds_y_size):  # 第一行中
            for j in range(self.raster_ds_x_size):
                px = self.raster_ds_geotrans[0] + j * self.raster_ds_geotrans[1] + i * self.raster_ds_geotrans[2]
                py = self.raster_ds_geotrans[3] + j * self.raster_ds_geotrans[4] + i * self.raster_ds_geotrans[5]
                coords = ct.TransformPoint(px, py)
                _pixel_location.append(coords[:2])
        _latitude_list = []
        _longitude_list = []
        for item in _pixel_location:
            _latitude_list.append(item[1])
            _longitude_list.append(item[0])
        return _latitude_list, _longitude_list

    def ReadRasterProjCoordinate(self):
        print('正在读取投影坐标信息'.center(20, '-'))
        _x_list = []
        _y_list = []
        for i in range(self.raster_ds_y_size):  # 第一行中
            for j in range(self.raster_ds_x_size):
                px = self.raster_ds_geotrans[0] + j * self.raster_ds_geotrans[1] + i * self.raster_ds_geotrans[2]
                py = self.raster_ds_geotrans[3] + j * self.raster_ds_geotrans[4] + i * self.raster_ds_geotrans[5]
                _x_list.append(px)
                _y_list.append(py)
        return _x_list, _y_list

    def WriteRasterFile(self, raster_ds_data, _output_path, _nodata=None):
        print('正在写出栅格文件...')
        if os.path.exists(_output_path):
            shutil.rmtree(_output_path)
            print('正在删除已存在文件夹')
        os.makedirs(_output_path)
        output_name = os.path.splitext(os.path.split(_output_path)[-1])[0] + '.tif'
        driver = gdal.GetDriverByName('GTIFF')
        write_ds = driver.Create(os.path.join(_output_path, output_name), self.raster_ds_x_size, self.raster_ds_y_size,
                                 1, gdal.GDT_Float32,
                                 options=["INTERLEAVE=PIXEL"])
        write_ds.SetGeoTransform(self.raster_ds_geotrans)
        write_ds.SetProjection(self.raster_ds_proj)
        # 写入数据
        output_band = write_ds.GetRasterBand(1)
        if _nodata is not None:
            output_band.SetNoDataValue(_nodata)
        output_band.WriteArray(raster_ds_data)
        write_ds.FlushCache()
        del write_ds
        print(f'栅格文件{output_name}写出完成.')


if __name__ == '__main__':
    dem_path = r'E:\Glacier_DEM_Register\Tanggula_ICESat2\10_XGBoost_Data\Result\NASADEM_Predict.tif'
    dem_predict = ReadRaster(dem_path)
    dem_data = dem_predict.ReadRasterFile()
    geoTransform = dem_predict.raster_ds_geotrans
    dem_point_data = SearchRasterRowColumnData(dem_data, [1500], [1500])
    latlon = dem_predict.ReadRasterLatLon()
    print(latlon)
