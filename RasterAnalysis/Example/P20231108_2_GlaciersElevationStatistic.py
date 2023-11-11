# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/8 19:43
# @Author : Hexk
# @Descript : 统计shp覆盖的DEM，计算平均高程、最大高程、最小高程
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles
import ReadRasterAndShape.ReadShape2DataFrame as RSDF
import RasterAnalysis.RasterStatisticRasterValueByIDRaster as RSRVBIDR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231108_8_DEM\20231108_8_DEM.tif"
    raster_id_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231108_5_GLACID_Raster\20231108_5_GLACID_Raster.tif'
    shape_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231108_4_RGI_AdvanceGlacierAndSeasonal_Dissolve\20231108_4_RGI_AdvanceGlacierAndSeasonal_Dissolve.shp"
    output_excel_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231108_7_Analysis_Excel'
    shape_rsdf = RSDF.ReadShape2DataFrame(shape_path)
    shape_df = shape_rsdf.ReadShapeFile()
    shape_df = shape_df.sort_values(by='GLACID', ascending=True)
    # 这一步需要转换成list来固定排列顺序，否则往下传递的时候会重新改变顺序
    glaciers_name = shape_df['Name'].aspect_values.tolist()
    excel_df = pd.DataFrame()
    csv_df = RSRVBIDR.RasterStatisticRasterValueByIDRaster(raster_path, raster_id_path)
    csv_df.insert(loc=1, column='Glaciers_Name', value=glaciers_name)
    output_excel_path = os.path.join(output_excel_folder, f'20231108_5_DEM.xlsx')
    csv_df.to_excel(output_excel_path)
