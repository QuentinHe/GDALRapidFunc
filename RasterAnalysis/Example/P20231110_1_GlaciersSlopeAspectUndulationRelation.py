# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/10 17:35
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import PathOperation.PathGetFiles as PGFiles
import RasterAnalysis.RasterStatisticRasterValueByIDRaster as RSRVBIDR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    change_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\5_YearChangeData\divide_SRTM_2019_2000\divide_SRTM_2019_2000.tif"
    aspect_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\AspectLevel_Mask.tif"
    undulation_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\Reclassify_Undulation_Mask.tif"
    slope_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\Reclassify_Slope_Mask.tif"
    output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis'
    # aspect_df = RSRVBIDR.RasterStatisticRasterValueByIDRaster(change_path, aspect_path, _output_csv_path=output_csv_path)
    undulation_df = RSRVBIDR.RasterStatisticRasterValueByIDRaster(change_path, undulation_path, _output_csv_path=os.path.join(output_csv_folder, f'Result_ElevationChangeWithUndulation.csv'))
    undulation_df = RSRVBIDR.RasterStatisticRasterValueByIDRaster(change_path, slope_path, _output_csv_path=os.path.join(output_csv_folder, f'Result_ElevationChangeWithSlope.csv'))
