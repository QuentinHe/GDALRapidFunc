# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/10/7 9:51
# @Author : Hexk
# @Descript : 对融合后的结果进行分级误差评定和综合误差评定，输出csv文件
import shutil
import PathOperation.PathGetFiles as PGF
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

if __name__ == '__main__':
    # RGI区域
    rgi_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseRGIRegion\3_Landsat8_RGI_2020.shp"
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
    nasa_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BasePoint\NASA'
    srtm_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BasePoint\SRTM'
    nasa_point_path_list, nasa_point_files_list = PGF.PathGetFiles(nasa_point_folder, '.shp')
    srtm_point_path_list, srtm_point_files_list = PGF.PathGetFiles(srtm_point_folder, '.shp')

    os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
    os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'

    """
    PART 3
    """
    # 分析Point位置的Error
    merge_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\1_PredictData\2_MergeData'
    output_error_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\2_CSVData\1_ErrorCSV'
    output_mask_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\1_PredictData\3_MaskData'
    output_change_csv_folder = os.path.join(
        r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\2_CSVData\2_ChangeCSV\20231007_Threshold30')
    if os.path.exists(output_change_csv_folder):
        shutil.rmtree(output_change_csv_folder)
        print('正在删除已存在CSV文件夹路径')
    os.makedirs(output_change_csv_folder)
    merge_predict_paths, merge_predict_files_list = PGF.PathGetFiles(merge_output_folder, '.tif')
    dem_type_list = ['NASA', 'SRTM']
    years_list = [i for i in range(2019, 2023)]
    bin_list = [i * 50 for i in range(1, 5)]
    point_path, merge_predict_path, raster_reclassify_path = None, None, None
    for dem_index, dem_item in enumerate(dem_type_list):
        for year_index, year_item in enumerate(years_list):
            for bin_index, bin_item in enumerate(bin_list):
                # 寻找Point File Path
                if dem_item == 'NASA':
                    print('正在执行NASA部分...')
                    # 找到对应的point_path
                    for point_files_index, point_files_item in enumerate(nasa_point_files_list):
                        if dem_item in point_files_item and str(
                                year_item) in point_files_item and f'Bin_{bin_item}' in point_files_item:
                            print(f'当前执行条件为:{dem_item} {year_item} {bin_item}'
                                  f'已找到文件名为:{point_files_item}')
                            point_path = nasa_point_path_list[point_files_index]
                            break
                        else:
                            print(f'ERROR: 不存在符合条件为:{dem_item} {year_item} {bin_item}的Point Shape文件.')
                    for dem_productions_index, dem_productions_item in enumerate(nasa_files_list):
                        if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
                            print(f'已经找到{dem_item}的Reclassify文件,等级{bin_item}.')
                            raster_reclassify_path = nasa_path_list[dem_productions_index]
                    for merge_predict_index, merge_predict_item in enumerate(merge_predict_files_list):
                        if dem_item in merge_predict_item and str(
                                year_item) in merge_predict_item and f'_{bin_item}' in merge_predict_item:
                            print(f'已经找到{dem_item}的Merge文件,等级{bin_item}.')
                            merge_predict_path = merge_predict_paths[merge_predict_index]
                elif dem_item == 'SRTM':
                    print('正在执行SRTM部分...')
                    # 找到对应的point_path
                    for point_files_index, point_files_item in enumerate(srtm_point_files_list):
                        if dem_item in point_files_item and str(
                                year_item) in point_files_item and f'Bin_{bin_item}' in point_files_item:
                            print(f'当前执行条件为:{dem_item} {year_item} {bin_item}'
                                  f'已找到文件名为:{point_files_item}')
                            point_path = srtm_point_path_list[point_files_index]
                            break
                        else:
                            print(f'ERROR: 不存在符合条件为:{dem_item} {year_item} {bin_item}的Point Shape文件.')
                    for dem_productions_index, dem_productions_item in enumerate(srtm_files_list):
                        if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
                            print(f'已经找到{dem_item}的Reclassify文件,等级{bin_item}.')
                            raster_reclassify_path = srtm_path_list[dem_productions_index]
                    for merge_predict_index, merge_predict_item in enumerate(merge_predict_files_list):
                        if dem_item in merge_predict_item and str(
                                year_item) in merge_predict_item and f'_{bin_item}' in merge_predict_item:
                            print(f'已经找到{dem_item}的Merge文件,等级{bin_item}.')
                            merge_predict_path = merge_predict_paths[merge_predict_index]
                else:
                    print('dem_type存在错误，请检查基准DEM的命名。')

                csv_output_path = os.path.join(output_error_csv_folder,
                                               f'ErrorAnalysis_{dem_item}_{year_item}_Bin_{bin_item}')
                IXGBR.AnalysisResult(point_path, merge_predict_path, raster_reclassify_path, f'Bin_{bin_item}',
                                     year_item,
                                     _dem_type=dem_item,
                                     _output_csv_folder=csv_output_path)

                output_mask_path = os.path.join(output_mask_folder, f'Mask_{dem_item}_{year_item}_Bin_{bin_item}')
                IXGBR.MaskRegionAnalysis(rgi_path, merge_predict_path, output_mask_path, raster_reclassify_path,
                                         _dem_type=dem_item,
                                         _bin_level=f'Bin_{bin_item}', _year=year_item,
                                         _output_csv_folder=output_change_csv_folder, _threshold=30)
