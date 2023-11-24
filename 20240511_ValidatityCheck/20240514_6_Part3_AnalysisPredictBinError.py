# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2024/5/14 下午9:13
# @Author : Hexk
# @Descript :

import shutil
import PathOperation.PathGetFiles as PGF
import PathOperation.PathFilesOperation as PFO
import XGBoostRegression.IntegrationXGBoostRegression as IXGBR
import os

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'
if __name__ == '__main__':
    """
    PART 3
    """

    # RGI区域
    rgi_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\1_GlaciersRegion\1_GlaciersRegion.shp"
    # 基准DEM
    srtm_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\4_BaseSRTMDEM'
    srtm_path_list, srtm_name_list = PGF.PathGetFiles(srtm_folder, '.tif')
    # SRTM数据
    dem_production_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\5_BaseDEMProductions'
    dem_production_list, dem_production_name_list = PGF.PathGetFiles(dem_production_folder, '.tif')
    # 公共数据
    # 公共数据只有projx projy
    common_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\CommonData'
    common_path_list, common_files_list = PGF.PathGetFiles(common_folder, '.tif')
    # Point数据
    srtm_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\11_Merge_Point'
    srtm_point_path_list, srtm_point_files_list = PGF.PathGetFiles(srtm_point_folder, '.shp')

    # 分析Point位置的Error
    merge_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\13_Merge_Data'
    output_error_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\18_Merge_Predict_Error_CSV'
    output_mask_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\14_Mask_Data'
    output_change_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Supplement_20240513\19_Merge_Predict_Change_CSV'

    merge_predict_paths, merge_predict_files_list = PGF.PathGetFiles(merge_output_folder, '.tif')
    bin_list = ['B50', 'B100', 'B150', 'B200']
    bin_num_list = ['50', '100', '150', '200']
    ctype_list_abb = ['M5', 'M10', 'P5', 'P10', 'R5', 'R10']
    ctype_list = ['Minus5', 'Minus10', 'Plus5', 'Plus10', 'Random5', 'Random10']
    point_path, merge_predict_path, raster_reclassify_path = None, None, None
    for bin_index, bin_item in enumerate(bin_list):
        for ctype_index, ctype_item in enumerate(ctype_list_abb):
            for point_files_index, point_files_item in enumerate(srtm_point_files_list):
                if bin_item in point_files_item and ctype_item in point_files_item:
                    print(f'当前执行条件为:{bin_item} {ctype_item}'
                          f'已找到文件名为:{point_files_item}')
                    point_path = srtm_point_path_list[point_files_index]
                    break
                else:
                    print(f'ERROR: 不存在符合条件为:{bin_item} {ctype_item}的Point Shape文件.')
            for dem_production_index, dem_production_item in enumerate(dem_production_name_list):
                if f'Reclassify{bin_num_list[bin_index]}' in dem_production_item and ctype_list[ctype_index] in dem_production_item:
                    print(f'当前执行条件为:{bin_item} {ctype_list[ctype_index]}'
                          f'已找到文件名为:{dem_production_item}')
                    raster_reclassify_path = dem_production_list[dem_production_index]
                    break
                else:
                    print(f'ERROR: 不存在符合条件为:{bin_item} {ctype_item}的Reclassify文件.')
            for merge_predict_index, merge_predict_item in enumerate(merge_predict_files_list):
                if ctype_item in merge_predict_item and bin_item in merge_predict_item:
                    print(f'已经找到{ctype_item} {bin_item}的Merge文件.')
                    merge_predict_path = merge_predict_paths[merge_predict_index]
                    break
                else:
                    print(f'ERROR: 不存在符合条件为:{bin_item} {ctype_item}的merge_predict_path文件.')

            csv_output_path = os.path.join(output_error_csv_folder,
                                           f'ErrorAnalysis_{bin_item}_{ctype_item}')
            IXGBR.AnalysisMultipleResult(point_path, merge_predict_path, raster_reclassify_path,
                                         f'{bin_item}_{ctype_item}',
                                         f'{ctype_item}',
                                         2020,
                                         _output_csv_folder=csv_output_path)

            output_mask_path = os.path.join(output_mask_folder, f'Mask_{bin_item}_{ctype_item}')
            PFO.MakeFolder(output_mask_path)
            output_mask_filepath = os.path.join(output_mask_path, f'Mask_{bin_item}_{ctype_item}.tif')
            IXGBR.MaskMultipleRegionAnalysis(rgi_path, merge_predict_path, output_mask_filepath, raster_reclassify_path,
                                             _bin_level=f'{bin_item}_{ctype_item}', _year=2020,
                                             _output_csv_folder=output_change_csv_folder)
