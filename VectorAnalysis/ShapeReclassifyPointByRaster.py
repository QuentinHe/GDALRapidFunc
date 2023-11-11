# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/11/21 10:47
# @Author : Hexk
# @Descript : 根据栅格值对Point进行重分类，注意栅格值是已经重分类过后的
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
import ReadRasterAndShape.ReadRaster as RR
import ReadRasterAndShape.ReadPoint2DataFrame as RPDF

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def ShapeReclassifyPointByRaster(_point_shape_path, _raster_path_list, _output_excel_path=None):
    print(''.center(30, '*'))
    print('正在执行函数ShapeReclassifyPointByRaster'.center(30, ' '))
    print('正在读取Point'.center(30, ' '))
    point_rsdf = RPDF.ReadPoint2DataFrame(_point_shape_path)
    point_df = point_rsdf.ReadShapeFile()
    print('正在读取Raster'.center(30, ' '))
    print(f'当前Raster_Path_List长度为:{len(_raster_path_list)}')
    for raster_path_index, raster_path_item in enumerate(_raster_path_list):
        raster_rr = RR.ReadRaster(raster_path_item)
        raster_data = raster_rr.ReadRasterFile()
        print(f'Raster:\n'
              f'Min{raster_rr.pixel_min},\n'
              f'Max{raster_rr.pixel_max},\n'
              f'Nodata{raster_rr.nodata},\n'
              f'Shape:{raster_rr.raster_ds_x_size, raster_rr.raster_ds_y_size}')
        # 设置dict的范围
        raster_dict = dict()
        for index in np.arange(int(raster_rr.pixel_min) - 1, int(raster_rr.pixel_max) + 1):
            raster_dict[index] = []
        # 找到Point在Raster上的位置
        point_row, point_column = point_rsdf.PointMatchRasterRowColumn(raster_rr.raster_ds_geotrans)
        # 往dict中添加值
        for index in range(len(point_row)):
            raster_dict[int(raster_data[point_row[index]][point_column[index]])].append(point_df['Delta_Ele'][index])
        if _output_excel_path:
            output_dict_key = []
            output_dict_mean = []
            output_dict_max = []
            output_dict_min = []
            for key, value in raster_dict.items():
                output_dict_key.append(key)
                output_dict_min.append(np.min(value))
                output_dict_max.append(np.max(value))
                output_dict_mean.append(np.mean(value))
            output_dict = {
                'Level': output_dict_key,
                'Mean': output_dict_mean,
                'Max': output_dict_max,
                'Min': output_dict_min
            }
            output_df = pd.DataFrame(output_dict)
            # 判断写入文件是否存在
            if not os.path.exists(_output_excel_path):
                # 不存在时
                print('文件不存在，正在创建'.center(30,' '))
                sheet_name = os.path.splitext(os.path.split(raster_path_item)[1])[0]
                output_df.to_excel(output_excel_path, sheet_name=sheet_name)
            else:
                # 存在
                print('文件存在，正在追加'.center(30, ' '))
                sheet_name = os.path.splitext(os.path.split(raster_path_item)[1])[0]
                with pd.ExcelWriter(output_excel_path, engine='openpyxl', mode='a') as writer:
                    output_df.to_excel(writer, sheet_name=sheet_name)
    return None


if __name__ == '__main__':
    aspect_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\AspectLevel_Mask.tif"
    undulation_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\Reclassify_Undulation_Mask.tif"
    slope_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis\3_Analysis_Data\20231110_1_DEM_Production\Reclassify_Slope_Mask.tif"
    point_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\1_PointData\11_MergePoint\SRTM_Bin_50\SRTM_Bin_50.shp"
    output_excel_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\1_Cartography\3_Analysis'
    output_excel_path = os.path.join(output_excel_folder, '20231121_1_ICESatExcel.xlsx')
    raster_path_list = [aspect_path, undulation_path, slope_path]
    ShapeReclassifyPointByRaster(point_path, raster_path_list, _output_excel_path=output_excel_path)
