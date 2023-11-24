# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/11 上午10:25
# @Author : Hexk
# @Descript : 估计值的偏差。估计值？就是 预测结果，这里对预测结果要做一个筛选，我要去除±20以上的像元，并将它们变成0，之后再分区统计bins，计算bins中的标准差。
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR
import RasterAnalysis.RasterClipByShape as RS
import time

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    merge_point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\1_PreTest_ICESat-2PointData\11_MergePoint\SRTM_Bin_50\SRTM_Bin_50.shp"
    # original_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Clip_SRTMDEM\SRTM_DEM_Clip.tif"
    estimate_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\4_MeanData\SRTM_2019.tif"
    # estimate_dem_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\4_MeanData\SRTM_Smooth3.tif"
    reclassify_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\2_PreTest_PredictData\1_Inter\3_MaskData\Mask_SRTM_2019_Bin_50\Mask_SRTM_2019_Bin_50\Reclassify\Reclassify.tif"
    _output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Pre_20240510\3_PreTest_CSV\7_TestCSV'
    # # ---
    # # 仅仅执行一次，裁剪DEM
    # clip_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Statistics_Data_20240511\Clip_SRTMDEM'
    # glacier_region_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\0_BaseRegion\1_GlaciersRegion\1_GlaciersRegion.shp"
    # output_clip_path = os.path.join(clip_path, 'SRTM_DEM_Clip.tif')
    # RS.RasterClipByShape(glacier_region_path, original_dem_path, output_clip_path)
    # # ---

    # original_dem_rr = RR.ReadRaster(original_dem_path)
    estimate_dem_rr = RR.ReadRaster(estimate_dem_path)
    reclassify_rr = RR.ReadRaster(reclassify_path)
    # original_dem_data = original_dem_rr.ReadRasterFile()
    estimate_dem_data = estimate_dem_rr.ReadRasterFile()
    reclassify_data = reclassify_rr.ReadRasterFile()
    bins_dict = dict()
    for i in range(int(np.min(reclassify_data)), int(np.max(reclassify_data) + 1)):
        bins_dict[i] = []
    valid_count = 0
    invalid_count = 0
    for y in range(estimate_dem_rr.raster_ds_y_size):
        for x in range(estimate_dem_rr.raster_ds_x_size):
            # bins_dict[int(reclassify_data[y][x])].append(raster_data[y][x])
            if -20 < estimate_dem_data[y][x] < 0 or 0 < estimate_dem_data[y][x] < 20:
                bins_dict[int(reclassify_data[y][x])].append(estimate_dem_data[y][x])
                valid_count += 1
            else:
                invalid_count += 1
    print(valid_count)
    print(invalid_count)
    bins_means = []
    bins_stds = []
    for i in bins_dict:
        bins_means.append(np.mean(bins_dict[i]))
        std = np.std(bins_dict[i])
        bins_stds.append(std)
        # bins_dh.append(20 * 20 / bin_length_list[i] * len(bins_dict[i]) / valid_count)
    csv_dict = {
        f'means': bins_means,
        f'stds': bins_stds,
    }
    csv_df = pd.DataFrame(csv_dict)
    df = pd.DataFrame()
    df = pd.concat([df, csv_df], axis=1)
    times = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
    output_path = os.path.join(_output_csv_folder, f'UncertaintyAnalysis_{times}.csv')
    df.to_csv(output_path)
