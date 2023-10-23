# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/17 9:26
# @Author : Hexk
# @Descript :
import os
import PathOperation.PathGetFiles as PGF
import numpy as np
import ReadRasterAndShape.ReadRaster as RR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    raster_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\3_MaskData'
    output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\4_MeanData'
    raster_paths_list, raster_files_list = PGF.PathGetFiles(raster_folder, '.tif')
    dem_list = ['NASA', 'SRTM']
    season_list = [i for i in range(1, 13)]
    for dem_index, dem_item in enumerate(dem_list):
        for season_index, season_item in enumerate(season_list):
            raster_means_list = []
            for files_index, files_item in enumerate(raster_files_list):
                if dem_item in files_item and f'Month{season_item}' == files_item.rsplit('_', 1)[1]:
                    print(f'已找到{files_item}的Raster文件Path:{raster_paths_list[files_index]}')
                    raster_means_list.append(raster_paths_list[files_index])
            print(f'开始计算平均{dem_item}...')
            raster_dict = dict()
            for index, item in enumerate(raster_means_list):
                raster_dict[index] = None
                raster_rr = RR.ReadRaster(item)
                raster_data = raster_rr.ReadRasterFile()
                raster_dict[index] = raster_data
            example_rr = RR.ReadRaster(raster_means_list[0])
            example_data = example_rr.ReadRasterFile()
            mean_data = np.zeros(example_data.shape)
            for i in range(len(raster_means_list)):
                mean_data += raster_dict[i]
            mean_data = mean_data / len(raster_means_list)
            output_path = os.path.join(output_folder, f'{dem_item}_Month{season_item}')
            example_rr.WriteRasterFile(mean_data, output_path, _nodata=0)
            del example_rr
