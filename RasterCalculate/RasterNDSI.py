# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/4 11:44
# @Author : Hexk

"""
    该文件实现NDSI的计算，并将0.2以上变成二值图，并转成矢量格式。
"""

from osgeo import gdal, ogr, osr
import os
import numpy as np
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = r'D:\Mambaforge\envs\mgdal_env\share\proj'
os.environ['GDAL_DATA'] = r'D:\Mambaforge\envs\mgdal_env\share'
np.seterr(divide='ignore', invalid='ignore')


class RasterCalculate:
    def __init__(self):
        self.ds_x_size = None
        self.ds_y_size = None
        self.ds_proj = None

    def CalculateNDSI(self, _band3_path, _band6_path):
        gdal.AllRegister()
        # 读取band3和band6
        _band3_ds = gdal.Open(_band3_path)
        _band6_ds = gdal.Open(_band6_path)
        _band3_ds_band = _band3_ds.GetRasterBand(1)
        _band6_ds_band = _band6_ds.GetRasterBand(1)

        _band3_ds_x_size = _band3_ds.RasterXSize  # 栅格矩阵的列数
        _band3_ds_y_size = _band3_ds.RasterYSize  # 栅格矩阵的行数
        _band3_ds_geotrans = _band3_ds.GetGeoTransform()  # 仿射矩阵，左上角像素的大地坐标和像素分辨率
        _band3_ds_proj = _band3_ds.GetProjection()  # 地图投影信息，字符串表示
        _band3_ds_data = _band3_ds_band.ReadAsArray()

        _band6_ds_x_size = _band6_ds.RasterXSize  # 栅格矩阵的列数
        _band6_ds_y_size = _band6_ds.RasterYSize  # 栅格矩阵的行数
        _band6_ds_geotrans = _band6_ds.GetGeoTransform()  # 仿射矩阵，左上角像素的大地坐标和像素分辨率
        _band6_ds_proj = _band6_ds.GetProjection()  # 地图投影信息，字符串表示
        _band6_ds_data = _band6_ds_band.ReadAsArray()
        # 判断band3和band6行列数是否相同
        if _band3_ds_x_size != _band6_ds_x_size or _band3_ds_y_size != _band6_ds_y_size:
            print(
                f'Error 两幅影像行列数不相同: Band1{(_band3_ds_x_size, _band3_ds_y_size)}; Band2{(_band6_ds_x_size, _band6_ds_y_size)}')
        self.ds_x_size = _band3_ds_x_size
        self.ds_y_size = _band3_ds_y_size
        self.ds_proj = _band3_ds_proj
        self.ds_geotrans = _band3_ds_geotrans

        _band3_np_data = np.array(_band3_ds_data)
        _band6_np_data = np.array(_band6_ds_data)
        # _band_ndsi = np.divide(np.subtract(_band3_np_data, _band6_np_data), np.add(_band3_np_data, _band6_np_data))
        # _band_ndsi = (_band3_np_data - _band6_np_data) / (_band3_np_data + _band6_np_data)

        _band_ndsi = (_band3_ds_data - _band6_ds_data) / (_band3_ds_data + _band6_ds_data)
        # 去除运算中的nan
        _band_ndsi_fillnan = np.nan_to_num(_band_ndsi, nan=0)
        # 去除运算后的inf
        _band_ndsi_fillnan[np.isinf(_band_ndsi_fillnan)] = 0
        return _band_ndsi_fillnan

    @staticmethod
    def RasterToBiplot(_band_data):
        np.putmask(_band_data, _band_data < 0.25, 0)
        np.putmask(_band_data, _band_data > 1, 0)
        np.putmask(_band_data, _band_data >= 0.25, 1)
        return _band_data

    @staticmethod
    def SieveFilterTheRaster(_band, threshold):
        connectedness = 8
        mask_path = 'none'
        input_band = _band
        output_band = input_band
        if mask_path == 'default':
            mask_band = input_band.GetMaskBand()
        elif mask_path == 'none':
            mask_band = None
        else:
            mask_ds = gdal.Open(mask_path)
            mask_band = mask_ds.GetRasterBand(1)
        prog_func = gdal.TermProgress_nocb
        result = gdal.SieveFilter(input_band, mask_band, output_band,
                                  threshold, connectedness,
                                  callback=prog_func)
        return result

    def BiplotRasterToVector(self, _band_data, _output_path, _output_prefix):
        _vector_projection = osr.SpatialReference()
        _vector_projection.ImportFromWkt(self.ds_proj)

        if os.path.exists(os.path.join(_output_path, _output_prefix)):
            os.remove(os.path.join(_output_path, _output_prefix))
        else:
            print(f'在当前输出目录下不存在文件夹.')
        os.makedirs(os.path.join(_output_path, _output_prefix))
        output_filename = f'{_output_prefix}.shp'

        shape_driver = ogr.GetDriverByName('ESRI Shapefile')
        shape_ds = shape_driver.CreateDataSource(os.path.join(_output_path, _output_prefix))
        layer = shape_ds.CreateLayer(output_filename, srs=_vector_projection, geom_type=ogr.wkbMultiPolygon)
        new_field = ogr.FieldDefn('Biplot', ogr.OFTReal)
        layer.CreateField(new_field)

        raster_driver = gdal.GetDriverByName('GTIFF')
        raster_output_name = f'{_output_prefix}.tif'
        write_ds = raster_driver.Create(os.path.join(_output_path, raster_output_name), self.ds_x_size, self.ds_y_size,
                                        1, gdal.GDT_Int16,
                                        options=["INTERLEAVE=PIXEL"])
        write_ds.SetGeoTransform(self.ds_geotrans)
        write_ds.SetProjection(self.ds_proj)
        # 写入数据
        write_ds.GetRasterBand(1).WriteArray(_band_data)
        raster_to_shape = write_ds.GetRasterBand(1)
        write_ds.FlushCache()

        gdal.Polygonize(raster_to_shape, None, layer, 0)
        shape_ds.SyncToDisk()
        shape_ds.Destroy()
        del write_ds
        print(f'文件{output_filename}写入完毕，存储路径为：{os.path.join(_output_path, output_filename)}')


    def WriteRaster(self, output_path, raster_ds_data):
        if os.path.exists(output_path):
            os.remove(output_path)
        else:
            print('已经覆盖原文件')
        driver = gdal.GetDriverByName('GTIFF')
        write_ds = driver.Create(output_path, self.ds_x_size, self.ds_y_size, 1, gdal.GDT_Float32,
                                 options=["INTERLEAVE=PIXEL"])
        write_ds.SetGeoTransform(self.ds_geotrans)
        write_ds.SetProjection(self.ds_proj)
        self.SieveFilterTheRaster(write_ds.GetRasterBand(1), 100)
        # 写入数据
        write_ds.GetRasterBand(1).WriteArray(raster_ds_data)
        write_ds.FlushCache()
        del write_ds


if __name__ == '__main__':
    # 2019
    # band3_path = (r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\0_Landsat8_2020'
    #               r'\LC08_L1TP_138037_20190810_20200827_02_T1\LC08_L1TP_138037_20190810_20200827_02_T1_B3.TIF')
    # band6_path = (r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\0_Landsat8_2020'
    #               r'\LC08_L1TP_138037_20190810_20200827_02_T1\LC08_L1TP_138037_20190810_20200827_02_T1_B6.TIF')
    # 2020
    # band3_path = (r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\0_Landsat8_2020'
    #               r'\LC08_L1TP_138037_20201031_20201106_02_T1\LC08_L1TP_138037_20201031_20201106_02_T1_B3.TIF')
    # band6_path = (r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\0_Landsat8_2020'
    #               r'\LC08_L1TP_138037_20201031_20201106_02_T1\LC08_L1TP_138037_20201031_20201106_02_T1_B6.TIF')
    # 2021
    # band3_path = (r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\0_Landsat8_2021'
    #               r'\LC08_L1TP_138037_20210714_20210721_02_T1\LC08_L1TP_138037_20210714_20210721_02_T1_B3.TIF')
    # band6_path = (r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\0_Landsat8_2021'
    #               r'\LC08_L1TP_138037_20210714_20210721_02_T1\LC08_L1TP_138037_20210714_20210721_02_T1_B6.TIF')
    # band3_path = (r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\0_Landsat8_2021'
    #               r'\LC08_L1TP_138037_20210730_20210804_02_T1\LC08_L1TP_138037_20210730_20210804_02_T1_B3.TIF')
    # band6_path = (r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\0_Landsat8_2021'
    #               r'\LC08_L1TP_138037_20210730_20210804_02_T1\LC08_L1TP_138037_20210730_20210804_02_T1_B6.TIF')
    # 2022
    band3_path = (r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\0_Landsat8_2022'
                  r'\LC09_L1TP_138037_20220826_20230401_02_T1\LC09_L1TP_138037_20220826_20230401_02_T1_B3.TIF')
    band6_path = (r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\0_Landsat8_2022'
                  r'\LC09_L1TP_138037_20220826_20230401_02_T1\LC09_L1TP_138037_20220826_20230401_02_T1_B6.TIF')

    calculator = RasterCalculate()
    ndsi_data = calculator.CalculateNDSI(band3_path, band6_path)
    ndsi_biplot = calculator.RasterToBiplot(ndsi_data)
    calculator.BiplotRasterToVector(ndsi_data,
                                    r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\1_Landsat8_2022_NDSI',
                                    '1_Landsat8_2022_Glaciers_2')
