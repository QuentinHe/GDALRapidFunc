# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/22 20:12
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadShape2DataFrame as RSDF
import RasterAnalysis.RasterStatisticRasterValueByIDRaster as RSRVBIDR
import PathOperation.PathGetFiles as PGFiles

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\4_MeanData'
    id_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\4_AnalysisRaster\2_Rasterize\Rasterize.tif"
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\4_AnalysisRaster\3_AnalysisCSV'
    raster_path_list, raster_name_list = PGFiles.PathGetFiles(raster_folder, '.tif')
    shape_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\0_BaseRegion\2_GlaciersRGIRegion\Tanggula_Region_RGI.shp"
    output_shape_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\4_AnalysisRaster\1_OutputRGIShape\OutputRGIShape.shp'
    polygon_rpdf = RSDF.ReadShape2DataFrame(shape_path)
    polygon_df = polygon_rpdf.ReadShapeFile()
    glacier_name = polygon_df['Name']
    for index, item in enumerate(raster_name_list):
        src_path = raster_path_list[index]
        df = RSRVBIDR.RasterStatisticRasterValueByIDRaster(src_path, id_path)
        df.insert(loc=1, column='Glaciers_Name', value=glacier_name)
        os.makedirs(os.path.join(output_csv_folder, item))
        output_csv_path = os.path.join(output_csv_folder, item, f'{item}.csv')
        df.to_csv(output_csv_path)

