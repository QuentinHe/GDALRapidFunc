# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/23 15:43
# @Author : Hexk
# @Descript :
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadShape2DataFrame as RSDF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    raster_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\4_MeanData\SRTM_2019\SRTM_2019.tif"
    glacid_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\1_Inter\4_MeanData\SRTM_2019\GLACID.tif"
    shape_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231108_2_Xu_AdvancGlacier\20231108_2_Xu_AdvancGlacier_Dissolve.shp'
    raster_rr = RR.ReadRaster(raster_path)
    glacid_rr = RR.ReadRaster(glacid_path)
    shape_rsdf = RSDF.ReadShape2DataFrame(shape_path)
    raster_data = raster_rr.ReadRasterFile()
    glacid_data = glacid_rr.ReadRasterFile()
    shape_df = shape_rsdf.ReadShapeFile()
    shape_df.sort_values('GLACID', inplace=True)
    shape_df = shape_df[['Name', 'GLACID']]
    glaciers_dict = dict()
    for index in np.arange(int(glacid_rr.pixel_min) - 1, int(glacid_rr.pixel_max) + 1):
        glaciers_dict[index] = []
    for y in range(raster_rr.raster_ds_y_size):
        for x in range(raster_rr.raster_ds_x_size):
            glaciers_dict[int(glacid_data[y][x])].append(raster_data[y][x])
    pixel_nums_list = [len(value) for key, value in glaciers_dict.items()]
    glaciers_mean = [np.mean(value)/19 for key, value in glaciers_dict.items()]
    glaciers_uncertainty = [np.std(value)/19 for key, value in glaciers_dict.items()]
    output_dict = dict(
        Glacier_ID=shape_df['Name'],
        PixelNums=pixel_nums_list[1:],
        GlacierMean=glaciers_mean[1:],
        Uncertainty=glaciers_uncertainty[1:]
    )
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\3_CSV\1_Inter\5_UncertaintyCSV'
    output_path = os.path.join(output_folder, 'SRTM_Uncertainty.xlsx')
    output_df = pd.DataFrame(output_dict)
    output_df.to_excel(output_path)
