# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/21 10:38
# @Author : Hexk
# @Descript :分析ICESat-2数据随坡度 坡向 起伏度 的变化情况，统计Point在Raster上的情况，并且将Raster Value放进Dict中
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


if __name__ == '__main__':
    # change_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\5_YearChangeData\divide_SRTM_2019_2000\divide_SRTM_2019_2000.tif"
    aspect_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\AspectLevel_Mask.tif"
    undulation_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\Reclassify_Undulation_Mask.tif"
    slope_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\Reclassify_Slope_Mask.tif"
    point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\11_MergePoint\SRTM_Bin_50\SRTM_Bin_50.shp"
