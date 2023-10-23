# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/16 18:19
# @Author : Hexk
# @Descript :

import shutil
import PathOperation.PathGetFiles as PGF
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    # RGI区域
    rgi_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\0_BaseRegion\1_GlaciersRegion\1_GlaciersRegion.shp"
    # 基准DEM
    dem_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEM'
    dem_path_list, dem_files_list = PGF.PathGetFiles(dem_folder, '.tif')
    # NASA数据
    nasa_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\NASA'
    nasa_path_list, nasa_files_list = PGF.PathGetFiles(nasa_folder, '.tif')
    # SRTM数据
    srtm_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\SRTM'
    srtm_path_list, srtm_files_list = PGF.PathGetFiles(srtm_folder, '.tif')
    # 公共数据
    common_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\CommonData'
    common_path_list, common_files_list = PGF.PathGetFiles(common_folder, '.tif')
    # Point数据
    # nasa_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BasePoint\NASA'
    nasa_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\13_MergeSeasonalPoint'
    # srtm_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BasePoint\SRTM'
    srtm_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\13_MergeSeasonalPoint'
    nasa_point_path_list, nasa_point_files_list = PGF.PathGetFiles(nasa_point_folder, '.shp')
    srtm_point_path_list, srtm_point_files_list = PGF.PathGetFiles(srtm_point_folder, '.shp')

    os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
    os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

    """
    PART 3
    """
    # 分析Point位置的Error
    merge_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\2_MergeData'
    output_error_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\3_CSV\2_Intra\2_SeasonaLErrorCSV'
    output_mask_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\2_PredictData\2_Intra\3_MaskData'
    output_change_csv_folder = os.path.join(
        r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\3_CSV\2_Intra\3_SeasonalChangeCSV')
    if os.path.exists(output_change_csv_folder):
        shutil.rmtree(output_change_csv_folder)
        print('正在删除已存在CSV文件夹路径')
    os.makedirs(output_change_csv_folder)
    merge_predict_paths, merge_predict_files_list = PGF.PathGetFiles(merge_output_folder, '.tif')
    dem_type_list = ['NASA', 'SRTM']
    bin_list = [i * 50 for i in range(1, 5)]
    season_list = [i for i in range(1, 13)]
    point_path, merge_predict_path, raster_reclassify_path = None, None, None
    for dem_index, dem_item in enumerate(dem_type_list):
        for bin_index, bin_item in enumerate(bin_list):
            for season_index, season_item in enumerate(season_list):
                # 寻找Point File Path
                if dem_item == 'NASA':
                    print('正在执行NASA部分...')
                    # 找到对应的point_path
                    for point_files_index, point_files_item in enumerate(nasa_point_files_list):
                        if dem_item in point_files_item and f'Bin_{bin_item}' in point_files_item and f'Month{season_item}' == \
                                point_files_item.rsplit('_', 1)[1]:
                            print(f'当前执行条件为:{dem_item}  {bin_item} Month{season_item}'
                                  f'已找到文件名为:{point_files_item}')
                            point_path = nasa_point_path_list[point_files_index]
                            break
                        else:
                            print(f'ERROR: 不存在符合条件为:{dem_item}  {bin_item}的Point Shape文件.')
                    for dem_productions_index, dem_productions_item in enumerate(nasa_files_list):
                        if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
                            print(f'已经找到{dem_item}的Reclassify文件,等级{bin_item}.')
                            raster_reclassify_path = nasa_path_list[dem_productions_index]
                    for merge_predict_index, merge_predict_item in enumerate(merge_predict_files_list):
                        tif_name = merge_predict_paths[merge_predict_index].split('\\')[8]
                        if dem_item in tif_name and f'Bin_{bin_item}' in tif_name and f'Month{season_item}' == \
                                tif_name.rsplit('_', 1)[1]:
                            print(f'已经找到{dem_item}的Merge文件,等级{bin_item}.')
                            merge_predict_path = merge_predict_paths[merge_predict_index]
                elif dem_item == 'SRTM':
                    print('正在执行SRTM部分...')
                    # 找到对应的point_path
                    for point_files_index, point_files_item in enumerate(srtm_point_files_list):
                        if dem_item in point_files_item and f'Bin_{bin_item}' in point_files_item and f'Month{season_item}' == \
                                point_files_item.rsplit('_', 1)[1]:
                            print(f'当前执行条件为:{dem_item} {bin_item} Month{season_item} '
                                  f'已找到文件名为:{point_files_item}')
                            point_path = srtm_point_path_list[point_files_index]
                            break
                        else:
                            print(f'ERROR: 不存在符合条件为:{dem_item} {bin_item}的Point Shape文件.')
                    for dem_productions_index, dem_productions_item in enumerate(srtm_files_list):
                        if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
                            print(f'已经找到{dem_item}的Reclassify文件,等级{bin_item}.')
                            raster_reclassify_path = srtm_path_list[dem_productions_index]
                    for merge_predict_index, merge_predict_item in enumerate(merge_predict_files_list):
                        tif_name = merge_predict_paths[merge_predict_index].split('\\')[8]
                        if dem_item in tif_name and f'Bin_{bin_item}' in tif_name and f'Month{season_item}' == \
                                tif_name.rsplit('_', 1)[1]:
                            print(f'已经找到{dem_item}的Merge文件,等级{bin_item}.')
                            merge_predict_path = merge_predict_paths[merge_predict_index]
                else:
                    print('dem_type存在错误，请检查基准DEM的命名。')

                csv_output_path = os.path.join(output_error_csv_folder,
                                               f'ErrorAnalysis_{dem_item}_Bin_{bin_item}_Month{season_item}')
                print(point_path)
                print(merge_predict_path)
                print(raster_reclassify_path)
                IXGBR.AnalysisResult(point_path, merge_predict_path, raster_reclassify_path, f'Bin_{bin_item}',
                                     2019,
                                     _dem_type=dem_item,
                                     _output_csv_folder=csv_output_path)

                output_mask_path = os.path.join(output_mask_folder,
                                                f'Mask_{dem_item}_Bin_{bin_item}_Month{season_item}')
                IXGBR.MaskRegionAnalysis(rgi_path, merge_predict_path, output_mask_path, raster_reclassify_path,
                                         _dem_type=dem_item,
                                         _bin_level=f'Bin_{bin_item}', _year=2019,
                                         _output_csv_folder=output_change_csv_folder)
