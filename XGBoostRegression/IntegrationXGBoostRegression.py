# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/9/18 20:22
# @Author : Hexk
# @Descript : 本文件是整合整个XGBoost回归预测，到结果分析全过程
import shutil
import time
import numpy as np
import pandas as pd
from osgeo import gdal, ogr, osr
import os
from sklearn import model_selection
import PathOperation.PathGetFiles as PGF
import ErrorAnalysis.ErrorAnalysis as EA
import ReadRasterAndShape.ReadPoint2DataFrame as RSDF
import ReadRasterAndShape.ReadRaster as RR
import PathOperation.PathFilesOperation as PFO
import XGBoostRegression.PredefineXGBoostRegression as PXGBR
import RasterAnalysis.RasterClipByShape as RSMR

os.environ['PROJ_LIB'] = 'D:/Mambaforge/envs/mgdal_env/Library/share/proj'
os.environ['GDAL_DATA'] = 'D:/Mambaforge/envs/mgdal_env/Library/share'


def IntegrationXGBoostRegression(_shape_path, _x_var, _y_var, _bin_level,
                                 _output_path,
                                 _raster_reclassify_path=None,
                                 _raster_slope_path=None,
                                 _raster_aspect_path=None,
                                 _raster_undulation_path=None,
                                 _raster_projx_path=None,
                                 _raster_projy_path=None):
    """
    实现了分段XGBoost回归。利用每个高程箱的点进行回归，并得到每个高程箱的拟合整体的结果。
    下一步需要读取reclassify，并根据每个像元的level，读取到指定结果中像元的值，融合成一个结果。
    :param _shape_path: point路径
    :param _x_var: 预测的x变量参数，shp point中的字段
    :param _y_var: y变量参数，shp point中的字段
    :param _bin_level: 指名是那个等级，需要在shp中有标记
    :param _output_path: 输出路径
    :param _raster_reclassify_path: reclassify栅格路径
    :param _raster_slope_path: slope栅格路径
    :param _raster_aspect_path: aspect栅格路径
    :param _raster_undulation_path: undulation栅格路径
    :param _raster_projx_path: projx栅格路径
    :param _raster_projy_path: projy栅格路径
    :return:
    """
    # 1. 读取矢量点和栅格文件
    # 2. 将值转换成list格式，后组成新的df
    # 3. XGBoost训练每一次的Bin分类
    # 4. 得到每一次等级预测的结果，输出每个等级预测的tif文件
    # 5. 按照Reclassify文件的值，从每个等级预测结果文件中读取指定像元的值，组成一副新的预测结果，并输出该结果；
    # 6. 重复上述操作直到Bin50 100 150 200的数据预测结果全部生成后，进行平均得到最终结果
    # 7. 掩膜栅格数据到RGI对应范围
    # 7. 分析：得到4年的最终结果。
    # ----------------
    # 本函数的用途是 实现2的后半部，3，4，5
    # ----------------
    print('正在执行IntegrationXGBoostRegression函数...')
    print('正在读取point数据'.center(30, '-'))
    point_rsdf = RSDF.ReadPoint2DataFrame(_shape_path)
    point_df = point_rsdf.ReadShapeFile()

    print('正在读取raster数据'.center(30, '-'))
    slope_data_list, aspect_data_list, undulation_data_list, reclassify_data_list, projx_data_list, projy_data_list, reclassify_rr = None, None, None, None, None, None, None
    if _raster_slope_path is not None:
        slope_rr = RR.ReadRaster(_raster_slope_path)
        slope_data = slope_rr.ReadRasterFile()
        print(f'slope:{slope_data.shape}')
        slope_data_list = slope_data.reshape(-1)
    if _raster_reclassify_path is not None:
        reclassify_rr = RR.ReadRaster(_raster_reclassify_path)
        reclassify_data = reclassify_rr.ReadRasterFile()
        print(f'reclassify:{reclassify_data.shape}')
        reclassify_data_list = reclassify_data.reshape(-1)
    if _raster_aspect_path is not None:
        aspect_rr = RR.ReadRaster(_raster_aspect_path)
        aspect_data = aspect_rr.ReadRasterFile()
        print(f'aspect:{aspect_data.shape}')
        aspect_data_list = aspect_data.reshape(-1)
    if _raster_undulation_path is not None:
        undulation_rr = RR.ReadRaster(_raster_undulation_path)
        undulation_data = undulation_rr.ReadRasterFile()
        print(f'undulation:{undulation_data.shape}')
        undulation_data_list = undulation_data.reshape(-1)
    if _raster_projx_path is not None:
        projx_rr = RR.ReadRaster(_raster_projx_path)
        projx_data = projx_rr.ReadRasterFile()
        print(f'projx:{projx_data.shape}')
        projx_data_list = projx_data.reshape(-1)
    if _raster_projy_path is not None:
        projy_rr = RR.ReadRaster(_raster_projy_path)
        projy_data = projy_rr.ReadRasterFile()
        print(f'projy:{projy_data.shape}')
        projy_data_list = projy_data.reshape(-1)

    print('正在进行数据格式转换...')
    point_df = RSDF.DataFrameFormatConvert(point_df,
                                           int_field=['Segment_ID', 'Aspect', 'Bin_50', 'Bin_100', 'Bin_150',
                                                      'Bin_200'],
                                           float_field=['Latitudes', 'Longitudes', 'H_Li', 'DEM_H', 'Delta_H',
                                                        'Undulation', 'Elevation', 'Slope', 'Proj_X', 'Proj_Y'])

    print('正在形成预测数据集...')
    predict_dict = dict(
        Slope=slope_data_list,
        Aspect=aspect_data_list,
        Undulation=undulation_data_list,
        Proj_X=projx_data_list,
        Proj_Y=projy_data_list,
    )
    predict_df = pd.DataFrame(predict_dict)

    print('正在形成训练集和验证集...')
    for i in range(min(point_df[_bin_level]), max(point_df[_bin_level]) + 1):
        temp_df = point_df.loc[point_df[_bin_level] == i]
        x_df = temp_df[_x_var]
        y_df = temp_df[_y_var]
        x_train, x_test, y_train, y_test, = model_selection.train_test_split(x_df, y_df, train_size=0.7)
        output_path = os.path.join(_output_path, f'{_bin_level}_{i}')
        output_name = _output_path.rsplit('\\', 1)[1] + f'{_bin_level}_{i}'
        output_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_Final_20231018\0_BaseData\3_CSV\2_Intra\1_XGBoostCSV'
        output_csv_path = os.path.join(output_csv_folder, output_name)
        PFO.MakeFolder(output_csv_path)
        _predict_data = PXGBR.XGBoostRegression(x_train, y_train, x_test, y_test, predict_df,
                                                _csv_output_path=output_csv_path)
        output_predict_data = np.array(_predict_data).reshape(reclassify_rr.raster_ds_y_size,
                                                              reclassify_rr.raster_ds_x_size)
        reclassify_rr.WriteRasterFile(output_predict_data, output_path)
    return None


def MergeRegressionClassify(_predict_folder_path, _raster_reclassify_path, _output_merge_folder, _dem_type=None,
                            _year=None):
    """
    融合得到的N个XGBOOST结果，需要搭配IntegrationXGBoostRegression函数使用
    :param _dem_type:
    :param _year:
    :param _output_merge_folder:
    :param _predict_folder_path: 预测结果的源文件夹
    :param _raster_reclassify_path: 分类依据文件
    :return: merge_data numpy.array格式，用于传递后续的分析.
    """
    print('正在执行MergeRegressionClassify...')
    path_list, files_list = PGF.PathGetFiles(_predict_folder_path, '.tif')
    files_prefix = files_list[0].rsplit('_', 1)[0]
    raster_rr = {}
    raster_data = {}
    print('正在读取需要融合的栅格...')
    for index, item in enumerate(files_list):
        raster_rr[item] = RR.ReadRaster(path_list[index])
        raster_data[item] = raster_rr[item].ReadRasterFile()
    raster_reclassify_rr = RR.ReadRaster(_raster_reclassify_path)
    raster_reclassify_data = raster_reclassify_rr.ReadRasterFile()
    print('正在匹配融合...')
    merge_data = np.empty(raster_reclassify_data.shape)
    for i in range(raster_reclassify_data.shape[0]):
        for j in range(raster_reclassify_data.shape[1]):
            merge_data[i][j] = raster_data[f'{files_prefix}_{int(raster_reclassify_data[i][j])}'][i][j]
    print('正在输出结果...')
    if _dem_type and _year is not None:
        output_path = os.path.join(_output_merge_folder, f'MergePredictResult_{_dem_type}_{_year}_{files_prefix}')
    else:
        output_path = os.path.join(_output_merge_folder, f'MergePredictResult_{files_prefix}')
    raster_reclassify_rr.WriteRasterFile(merge_data, output_path)
    return merge_data


def AnalysisResult(_shape_path: object, _raster_predict_path: object, _raster_reclassify_path: object,
                   _bin_level: object, _year: object, _dem_type: object,
                   _output_csv_folder: object = None) -> object:
    """
    该函数是针对点结果进行统计分析，包括分析MAE RMSE STD等信息，最后输出成一个csv表格，CSV可以记录年份和Bin Lv但是无法记录DEM。
    :param _dem_type:
    :param _shape_path: point点路径，
    :param _raster_predict_path: 预测结果数据路径
    :param _raster_reclassify_path: 分类栅格数据路径
    :param _bin_level: 指名等级，需要包含在shape文件的列中
    :param _year: 指名年份，int
    :param _output_csv_folder: 输出csv文件夹路径
    :return: None
    """
    # 分析讲究几个部分：
    # 1. 分箱分析RMSE、MAE、STD，总体分析MAE MSE RMSE STD
    # 2. 年变化，结果的dh，直接除以年份吧
    print('正在执行AnalysisResult...')
    point_rsdf = RSDF.ReadPoint2DataFrame(_shape_path)
    point_df = point_rsdf.ReadShapeFile()
    point_df[['Bin_50', 'Bin_100', 'Bin_150', 'Bin_200', 'Delta_Ele']] = point_df[
        ['Bin_50', 'Bin_100', 'Bin_150', 'Bin_200', 'Delta_Ele']].astype('float32')
    predict_rr = RR.ReadRaster(_raster_predict_path)
    predict_data = predict_rr.ReadRasterFile()
    print(predict_rr.raster_ds_geotrans)
    point_row, point_colum = point_rsdf.PointMatchRasterRowColumn(predict_rr.raster_ds_geotrans)
    predict_point_value = RR.SearchRasterRowColumnData(point_row, point_colum, _raster_ds_path=_raster_predict_path)
    point_df = pd.concat([point_df, pd.DataFrame(predict_point_value, columns=['Predict_DH'])], axis=1)

    delta_elevation_dict = dict()
    predict_dict = dict()
    for i in range(int(min(point_df[_bin_level])), int(max(point_df[_bin_level])) + 1):
        delta_elevation_dict[i] = []
        predict_dict[i] = []
    for index, item in enumerate(point_df[_bin_level]):
        delta_elevation_dict[int(item)].append(point_df['Delta_Ele'][index])
        predict_dict[int(item)].append(point_df['Predict_DH'][index])

    bin_rmse = []
    bin_mae = []
    bin_predict_mean = []
    bin_origin_mean = []
    bin_predict_std = []
    bin_origin_std = []
    for i in delta_elevation_dict:
        # 预测和实际结果的RMSE
        bin_rmse.append(EA.rmse(delta_elevation_dict[i], predict_dict[i]))
        # 预测和实际结果的MAE
        bin_mae.append(EA.mae(delta_elevation_dict[i], predict_dict[i]))
        # 实际结果的标准差
        bin_origin_std.append(np.std(delta_elevation_dict[i]))
        # 预测结果的标准差
        bin_predict_std.append(np.std(predict_dict[i]))
        # 预测结果的分箱均值
        bin_predict_mean.append(np.mean(predict_dict[i]) / (_year - 2000))
        # 实际结果的分箱均值
        bin_origin_mean.append(np.mean(delta_elevation_dict[i]) / (_year - 2000))
    total_mae = EA.mae(point_df['Delta_Ele'], point_df['Predict_DH'])
    total_mse = EA.mse(point_df['Delta_Ele'], point_df['Predict_DH'])
    total_rmse = EA.rmse(point_df['Delta_Ele'], point_df['Predict_DH'])

    print('分箱误差为:')
    for index, item in enumerate(bin_rmse):
        print(
            f'Bin:{index + 1}----RMSE:{item}, MAE:{bin_mae[index]}, Predict_STD:{bin_predict_std[index]}, Origin_DH_STD:{bin_origin_std[index]}')
        print(f'Predict_Mean:{bin_predict_mean[index]},Origin_Mean:{bin_origin_mean[index]}')
    print(f"总体误差为:"
          f"MAE:{total_mae}, RMSE:{total_rmse}")

    if _output_csv_folder is not None:
        csv_dict = dict(
            Bin_MAE=bin_mae,
            Total_MAE=total_mae,
            Bin_RMSE=bin_rmse,
            Total_RMSE=total_rmse,
            Bin_Origin_STD=bin_origin_std,
            Bin_Predict_STD=bin_predict_std,
            Bin_Origin_Mean=bin_origin_mean,
            Total_Origin_Mean=np.mean(bin_origin_mean),
            Bin_Predict_Mean=bin_predict_mean,
            Total_Predict_Mean=np.mean(bin_predict_mean),
        )
        csv_df = pd.DataFrame(csv_dict)
        times = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
        if os.path.exists(_output_csv_folder):
            shutil.rmtree(_output_csv_folder)
            print('正在删除已存在CSV文件夹路径')
        os.makedirs(_output_csv_folder)
        csv_path = os.path.join(_output_csv_folder, f'{_dem_type}_{_year}_{_bin_level}_{times}.csv')
        csv_df.to_csv(csv_path)
    return None


def MaskRegionAnalysis(_input_shape_path, _input_raster_path, _output_raster_folder, _raster_reclassify_path,
                       _dem_type,
                       _year,
                       _bin_level,
                       _threshold=50, _output_csv_folder=None):
    """
    掩膜输入的两个栅格，并分级统计均值。
    :param _dem_type:
    :param _input_shape_path: 输入裁剪的范围文件
    :param _input_raster_path: 输入裁剪的结果文件 predict
    :param _output_raster_folder: 输出文件的文件夹路径
    :param _raster_reclassify_path: 输入的栅格文件路径
    :param _year: 指定运行的年份日期
    :param _bin_level: 高程箱个数字段
    :param _threshold: 过滤阈值
    :param _output_csv_folder: 输出的csv文件夹路径
    :return: None
    """
    # 先掩膜结果，之后分区统计结果
    # 妈的，还要传递保存的路径
    # 掩膜Predict文件
    mask_path = RSMR.RasterClipByShape(_input_shape_path, _input_raster_path, _output_raster_folder)
    # 掩膜分类文件
    mask_reclassify_path = RSMR.RasterClipByShape(_input_shape_path, _raster_reclassify_path,
                                                  os.path.join(_output_raster_folder, 'Reclassify'))
    # 读取分类文件
    reclassify_rr = RR.ReadRaster(mask_reclassify_path)
    reclassify_data = reclassify_rr.ReadRasterFile()
    reclassify_data_list = reclassify_data.reshape(-1)
    # 读取掩膜后的结果
    mask_rr = RR.ReadRaster(mask_path)
    mask_data = mask_rr.ReadRasterFile()
    mask_data_list = mask_data.reshape(-1)

    predict_dict = dict()
    for i in range(int(min(reclassify_data_list)), int(max(reclassify_data_list)) + 1):
        predict_dict[i] = []
    for index, item in enumerate(reclassify_data_list):
        if mask_data_list[index] != 0 and np.abs(mask_data_list[index]) <= _threshold:
            predict_dict[item].append(mask_data_list[index])

    bin_mean = []
    for i in predict_dict:
        bin_mean.append(np.mean(predict_dict[i]) / (_year - 2000))
    new_bin_mean = [i for i in bin_mean if np.isnan(i) == False]
    if _output_csv_folder is not None:
        csv_dict = dict(
            Bin_Level=[i for i in range(int(min(reclassify_data_list)), int(max(reclassify_data_list)) + 1)],
            Means=bin_mean,
        )
        csv_df = pd.DataFrame(csv_dict)
        csv_df.loc[len(csv_df.index)] = ['TotalMean', np.mean(new_bin_mean)]
        times = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
        csv_path = os.path.join(_output_csv_folder,
                                f'MaskAnalysis_{_dem_type}_{_year}_{_bin_level}_threshold{_threshold}_{times}.csv')
        csv_df.to_csv(csv_path)
    return None


def MeanBinsRaster(_raster_folder, _output_path):
    """
    将多个栅格计算平均值，并输出
    :param _raster_folder: 栅格文件夹
    :param _output_path: 输出栅格的路径
    :return:
    """
    raster_paths_list, raster_files_list = PGF.PathGetFiles(_raster_folder, '.tif')
    raster_means_list = []
    dem_list = ['NASA', 'SRTM']
    # years_list = [i for i in range(2019, 2023)]
    years_list = [2019]
    for dem_index, dem_item in enumerate(dem_list):
        for years_index, years_item in enumerate(years_list):
            for files_index, files_item in enumerate(raster_files_list):
                if dem_item in files_item and str(years_item) in files_item:
                    print(f'已找到{files_item}的Raster文件Path:{raster_paths_list[files_index]}')
                    raster_means_list.append(raster_paths_list[files_index])
            print(f'开始计算平均{dem_item}_{years_item}...')
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
            output_path = os.path.join(_output_path, f'{dem_item}_{years_item}')
            example_rr.WriteRasterFile(mean_data, output_path, _nodata=0)
            del example_rr
    return None


def YearChangeAnalysis(_raster_folder, _reclassify_path, _output_raster_folder, _output_csv_folder, _threshold=50,
                       _mode=None):
    raster_paths_list, raster_files_list = PGF.PathGetFiles(_raster_folder, '.tif')
    dem_list = ['SRTM']
    years_list = [2019]
    reclassify_rr = RR.ReadRaster(_reclassify_path)
    reclassify_data = reclassify_rr.ReadRasterFile()
    for dem_index, dem_item in enumerate(dem_list):
        year_dh_path_list = []
        csv_dict = dict()
        total_means = []
        for years_index, years_item in enumerate(years_list):
            for files_index, files_item in enumerate(raster_files_list):
                if dem_item in files_item and str(years_item) in files_item:
                    print(f'已找到{files_item}的Raster文件Path:{raster_paths_list[files_index]}')
                    year_dh_path_list.append(raster_paths_list[files_index])
        result_data = np.zeros(reclassify_data.shape)
        for index, item in enumerate(year_dh_path_list):
            raster_rr = RR.ReadRaster(item)
            raster_data = raster_rr.ReadRasterFile()
            # 声明分级字典，用于储存年变化量
            bins_dict = dict()
            for i in range(int(np.min(reclassify_data)), int(np.max(reclassify_data) + 1)):
                bins_dict[i] = []
            # 年变化之间做差
            if index == 0:
                result_data += raster_data
                for y in range(reclassify_rr.raster_ds_y_size):
                    for x in range(reclassify_rr.raster_ds_x_size):
                        if np.abs(result_data[y][x]) <= _threshold:
                            bins_dict[int(reclassify_data[y][x])].append(result_data[y][x])
                bin_mean = []
                for i in bins_dict:
                    bin_mean.append(np.mean(bins_dict[i]) / (years_list[index] - 2000))
                bin_means_nonan = [i for i in bin_mean if np.isnan(i) == False and i != 0]
                csv_dict[years_list[index]] = bin_means_nonan
                total_means.append(np.mean(bin_means_nonan))
                if _mode is not None:
                    output_raster_path = os.path.join(_output_raster_folder,
                                                      f"{_mode}_{dem_item}_{years_list[index]}_2000")
                else:
                    output_raster_path = os.path.join(_output_raster_folder, f"{dem_item}_{years_list[index]}_2000")
                reclassify_rr.WriteRasterFile(result_data / (years_list[index] - 2000), output_raster_path, _nodata=0)
            elif index != 0:
                if _mode is None:
                    discrepancy_data = raster_data - result_data
                else:
                    discrepancy_data = raster_data / (years_list[index] - 2000)
                # 按照分级将做差后的数据添加到Bin Dict中
                for y in range(reclassify_rr.raster_ds_y_size):
                    for x in range(reclassify_rr.raster_ds_x_size):
                        if np.abs(result_data[y][x]) <= _threshold:
                            bins_dict[int(reclassify_data[y][x])].append(discrepancy_data[y][x])
                if _mode is not None:
                    output_raster_path = os.path.join(_output_raster_folder,
                                                      f"{_mode}_{dem_item}_{years_list[index]}_{years_list[index - 1]}")
                else:
                    output_raster_path = os.path.join(_output_raster_folder,
                                                      f"{dem_item}_{years_list[index]}_{years_list[index - 1]}")
                raster_rr.WriteRasterFile(discrepancy_data, output_raster_path, _nodata=0)
                del raster_rr
                bin_mean = []
                bin_std = []
                for i in bins_dict:
                    bin_mean.append(np.mean(bins_dict[i]))
                    bin_std.append(np.std(bins_dict[i]))
                bin_means_nonan = [i for i in bin_mean if np.isnan(i) == False and i != 0]
                bin_stds_nonan = [i for i in bin_std if np.isnan(i) == False and i != 0]
                csv_dict[years_list[index]] = bin_means_nonan
                total_means.append(np.mean(bin_means_nonan))
        csv_df = pd.DataFrame(csv_dict)
        csv_df.loc[len(csv_df.index)] = total_means
        times = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
        if _mode is None:
            _output_csv_path = os.path.join(_output_csv_folder, f'{dem_item}_th{_threshold}_{times}.csv')
        else:
            _output_csv_path = os.path.join(_output_csv_folder, f'{_mode}_{dem_item}_th{_threshold}_{times}.csv')
        csv_df.to_csv(_output_csv_path)
    del reclassify_rr
    return None


def SeasonalChangeAnalysis(_raster_path_list, _reclassify_path, _output_csv_folder, _output_csv_name, _threshold=50):
    reclassify_rr = RR.ReadRaster(_reclassify_path)
    reclassify_data = reclassify_rr.ReadRasterFile()
    csv_dict = dict()
    total_means = []
    for raster_path_index, raster_path_item in enumerate(_raster_path_list):
        bins_dict = dict()
        for i in range(int(np.min(reclassify_data)), int(np.max(reclassify_data) + 1)):
            bins_dict[i] = []
        raster_rr = RR.ReadRaster(raster_path_item)
        raster_data = raster_rr.ReadRasterFile()
        for y in range(reclassify_rr.raster_ds_y_size):
            for x in range(reclassify_rr.raster_ds_x_size):
                if np.abs(raster_data[y][x]) <= _threshold:
                    bins_dict[int(reclassify_data[y][x])].append(raster_data[y][x])
        bin_mean = []
        bin_std = []
        for i in bins_dict:
            bin_mean.append(np.mean(bins_dict[i]))
            bin_std.append(np.std(bins_dict[i]))
        bin_means_nonan = [i for i in bin_mean if np.isnan(i) == False and i != 0]
        csv_dict_name = os.path.splitext(os.path.split(raster_path_item)[1])[0]
        csv_dict[f'{csv_dict_name}_Means'] = bin_means_nonan
        total_means.append(np.mean(bin_means_nonan))
    csv_df = pd.DataFrame(csv_dict)
    csv_df.loc[len(csv_df.index)] = total_means
    times = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
    output_csv_path = os.path.join(_output_csv_folder, f'{_output_csv_name}.csv')
    csv_df.to_csv(output_csv_path)
    return None


def ElevationUncertaintyAnalysis(_raster_folder: object, _raster_reclassify_path: object,
                                 _output_csv_folder: object) -> object:
    # 这里不再做差，就除以年份
    raster_paths_list, raster_files_list = PGF.PathGetFiles(_raster_folder, '.tif')
    dem_list = ['SRTM']
    reclassify_rr = RR.ReadRaster(_raster_reclassify_path)
    reclassify_data = reclassify_rr.ReadRasterFile()
    # 循环读取不同年份的数据
    for dem_index, dem_item in enumerate(dem_list):
        df = pd.DataFrame()
        for file_index, file_item in enumerate(raster_files_list):
            if dem_item in file_item:
                print(f'已找到{file_item}的Raster文件Path:{raster_paths_list[file_index]}')
                file_path = raster_paths_list[file_index]
                # 读取DH数据
                raster_rr = RR.ReadRaster(file_path)
                raster_data = raster_rr.ReadRasterFile()
                # 按照reclassify划分data分级
                bins_dict = dict()
                for i in range(int(np.min(reclassify_data)), int(np.max(reclassify_data) + 1)):
                    bins_dict[i] = []
                for y in range(reclassify_rr.raster_ds_y_size):
                    for x in range(reclassify_rr.raster_ds_x_size):
                        bins_dict[int(reclassify_data[y][x])].append(raster_data[y][x])
                # 开始统计分析
                # 计算标准差
                bins_means = []
                bins_stds = []
                bins_3stds = []
                bins_ce = []
                bins_filter3stds_means = []
                for i in bins_dict:
                    bins_means.append(np.mean(bins_dict[i]))
                    std = np.std(bins_dict[i])
                    bins_stds.append(std)
                    bins_3stds.append(std * 3)
                    bins_ce.append(np.sqrt(np.power(np.std(bins_dict[i]), 2) + np.power(20, 2)))
                    temp_list = []
                    for j in bins_dict[i]:
                        if np.abs(j) < std * 3:
                            temp_list.append(j)
                    bins_filter3stds_means.append(np.mean(temp_list))
                year_item = 2019
                csv_dict = {
                    'Bins': [i for i in range(int(np.min(reclassify_data)), int(np.max(reclassify_data) + 1))],
                    f'{year_item}_means': bins_means,
                    f'{year_item}_stds': bins_stds,
                    f'{year_item}_3stds': bins_3stds,
                    f'{year_item}_ce': bins_ce,
                    f'{year_item}_filter3stds_means': bins_filter3stds_means,
                }
                csv_df = pd.DataFrame(csv_dict)
                df = pd.concat([df, csv_df], axis=1)
        times = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
        output_path = os.path.join(_output_csv_folder, f'{dem_item}_UncertaintyAnalysis_{times}.csv')
        df.to_csv(output_path)
    return None

if __name__ == '__main__':
    # shape_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20230916\1_FilterOutliers\1_FilterOutliers\NASA_2019_Bin_50\NASA_2019_Bin_50.shp'
    # raster_folder_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20230916\1_RasterData'
    # # ------PART 1------
    # IntegrationXGBoostRegression(shape_path,
    #                              ['Slope', 'Aspect', 'Undulation', 'Proj_X', 'Proj_Y'],
    #                              ['Delta_Ele'],
    #                              'Bin_50',
    #                              _output_folder=r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231003\Predict',
    #                              _raster_slope_path=r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\1_DEM_Aspect\NASA_Aspect_Level\NASA_Aspect_Level.tif",
    #                              _raster_undulation_path=r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\3_DEM_Undulation\NASA\3_NASA_Undulation.tif",
    #                              _raster_aspect_path=r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\1_DEM_Aspect\NASA_DEM\1_NASA_Aspect.tif",
    #                              _raster_reclassify_path=r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\NASA_Reclassify_50\NASA_Reclassify_50.tif",
    #                              _raster_projx_path=r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\4_DEM_ProjCoords\ProjX\ProjX.tif",
    #                              _raster_projy_path=r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\4_DEM_ProjCoords\ProjY\ProjY.tif")
    # # ------PART 2------
    # predict_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231003\Predict'
    # MergeRegressionClassify(predict_path,
    #                         _raster_reclassify_path=r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\NASA_Reclassify_50\NASA_Reclassify_50.tif",
    #                         _dem_type='NASA',
    #                         _output_merge_folder=r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231003')
    # ------PART 3------
    predict_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231003\MergePredictResult_Bin_50\MergePredictResult_Bin_50.tif"
    predict_rr = RR.ReadRaster(predict_path)
    predict_data = predict_rr.ReadRasterFile()
    reclassify_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\DEM_Process\2_DEM_Reclassify\NASA_Reclassify_50\NASA_Reclassify_50.tif'
    output_csv_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231003\Analysis_CSV'
    # AnalysisResult(shape_path, predict_data, reclassify_path, 'Bin_50', 2019, output_csv_path)
    # ------PART 4------
    region_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\0_Landsat8\3_Landsat8_RGI_FourYear\3_Landsat8_RGI_2020.shp"
    output_mask_path = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231003\3_Mask_PredictResult\2019_Bin_50'
    MaskRegionAnalysis(region_path, predict_path, output_mask_path, reclassify_path, _bin_level='Bin_50', _year=2019,
                       _output_csv_folder=output_csv_path, _threshold=30, _dem_type='NASA')
    # """
    # 第一遍跑通完毕，接下来是整理一下4年运行的数据。
    # """
    # # RGI区域
    # rgi_path = r"E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseRGIRegion\3_Landsat8_RGI_2020.shp"
    # # 基准DEM
    # dem_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEM'
    # dem_path_list, dem_files_list = PGFiles.PathGetFiles(dem_folder, '.tif')
    # # NASA数据
    # nasa_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\NASA'
    # nasa_path_list, nasa_files_list = PGFiles.PathGetFiles(nasa_folder, '.tif')
    # # SRTM数据
    # srtm_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\SRTM'
    # srtm_path_list, srtm_files_list = PGFiles.PathGetFiles(srtm_folder, '.tif')
    # # 公共数据
    # common_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BaseDEMProductions\CommonData'
    # common_path_list, common_files_list = PGFiles.PathGetFiles(common_folder, '.tif')
    # # Point数据
    # nasa_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BasePoint\NASA'
    # srtm_point_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\0_BaseData\BasePoint\SRTM'
    # nasa_point_path_list, nasa_point_files_list = PGFiles.PathGetFiles(nasa_point_folder, '.shp')
    # srtm_point_path_list, srtm_point_files_list = PGFiles.PathGetFiles(srtm_point_folder, '.shp')
    #
    # # """
    # # PART 1
    # # """
    # # # 先循环NASA，再循环SRTM
    # # # 循环年份
    # # # 循环某一年的bin
    # # xgboost_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\1_PredictData\1_XGBoostData'
    # # # 循环DEM， 先NASA，再SRTM
    # # for dem_index, dem_item in enumerate(dem_path_list):
    # #     dem_type = dem_files_list[dem_index].split('_')[0]  # NASA or SRTM
    # #     # dem_type = 'SRTM'
    # #     # 循环年份
    # #     for year_index, year_item in enumerate([i for i in range(2019, 2023)]):
    # #         # 循环Bin等级
    # #         for bin_index, bin_item in enumerate([i * 50 for i in range(1, 5)]):
    # #             # 寻找Point File Path
    # #             point_path = None
    # #             if dem_type == 'NASA':
    # #                 print('正在执行NASA部分...')
    # #                 # 找到对应的point_path
    # #                 for point_files_index, point_files_item in enumerate(nasa_point_files_list):
    # #                     if dem_type in point_files_item and str(
    # #                             year_item) in point_files_item and f'Bin_{bin_item}' in point_files_item:
    # #                         print(f'当前执行条件为:{dem_type} {year_item} {bin_item}'
    # #                               f'已找到文件名为:{point_files_item}')
    # #                         point_path = nasa_point_path_list[point_files_index]
    # #                         break
    # #                     else:
    # #                         print(f'ERROR: 不存在符合条件为:{dem_type} {year_item} {bin_item}的Point Shape文件.*')
    # #             elif dem_type == 'SRTM':
    # #                 print('正在执行SRTM部分...')
    # #                 # 找到对应的point_path
    # #                 for point_files_index, point_files_item in enumerate(srtm_point_files_list):
    # #                     if dem_type in point_files_item and str(
    # #                             year_item) in point_files_item and f'Bin_{bin_item}' in point_files_item:
    # #                         print(f'当前执行条件为:{dem_type} {year_item} {bin_item}'
    # #                               f'已找到文件名为:{point_files_item}')
    # #                         point_path = srtm_point_path_list[point_files_index]
    # #                         break
    # #                     else:
    # #                         print(f'ERROR: 不存在符合条件为:{dem_type} {year_item} {bin_item}的Point Shape文件.')
    # #             else:
    # #                 print('dem_type存在错误，请检查基准DEM的命名。')
    # #
    # #             # 生成bin字段
    # #             bin_level = f'Bin_{bin_item}'
    # #
    # #             # 生成输出预测结果的路径
    # #             xgboost_output_path = os.path.join(xgboost_output_folder, f'{dem_type}_{year_item}_{bin_level}')
    # #             if os.path.exists(xgboost_output_path):
    # #                 shutil.rmtree(xgboost_output_path)
    # #                 print('正在删除已存在文件夹')
    # #             os.makedirs(xgboost_output_path)
    # #             print(f'已创建{dem_type}_{year_item}_{bin_level}的输出文件夹.')
    # #
    # #             # 找到其他DEM输入参数的路径
    # #             raster_slope_path, raster_aspect_path, raster_undulation_path, raster_reclassify_path = None, None, None, None
    # #             raster_projx_path = None
    # #             raster_projy_path = None
    # #             for proj_index, proj_item in enumerate(common_files_list):
    # #                 if 'X' in proj_item:
    # #                     raster_projx_path = common_path_list[proj_index]
    # #                     print(f'已经找到{dem_type}的Proj X文件')
    # #                 elif 'Y' in proj_item:
    # #                     raster_projy_path = common_path_list[proj_index]
    # #                     print(f'已经找到{dem_type}的Proj Y文件')
    # #             if dem_type == 'NASA' or 'nasa':
    # #                 print('正在寻找NASA的相关DEM产品路径...')
    # #                 for dem_productions_index, dem_productions_item in enumerate(nasa_files_list):
    # #                     if 'Slope' in dem_productions_item:
    # #                         print(f'已经找到{dem_type}的Slope文件.')
    # #                         raster_slope_path = nasa_path_list[dem_productions_index]
    # #                     elif 'Aspect' in dem_productions_item:
    # #                         print(f'已经找到{dem_type}的Aspect文件.')
    # #                         raster_aspect_path = nasa_path_list[dem_productions_index]
    # #                     elif 'Undulation' in dem_productions_item:
    # #                         print(f'已经找到{dem_type}的Undulation文件.')
    # #                         raster_undulation_path = nasa_path_list[dem_productions_index]
    # #                     elif 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
    # #                         print(f'已经找到{dem_type}的Reclassify文件,等级{bin_item}.')
    # #                         raster_reclassify_path = nasa_path_list[dem_productions_index]
    # #             elif dem_type == 'SRTM' or 'srtm':
    # #                 print('正在寻找SRTM的相关DEM产品路径...')
    # #                 for dem_productions_index, dem_productions_item in enumerate(srtm_files_list):
    # #                     if 'Slope' in dem_productions_item:
    # #                         print(f'已经找到{dem_type}的Slope文件.')
    # #                         raster_slope_path = srtm_path_list[dem_productions_index]
    # #                     elif 'Aspect' in dem_productions_item:
    # #                         print(f'已经找到{dem_type}的Aspect文件.')
    # #                         raster_aspect_path = srtm_path_list[dem_productions_index]
    # #                     elif 'Undulation' in dem_productions_item:
    # #                         print(f'已经找到{dem_type}的Undulation文件.')
    # #                         raster_undulation_path = srtm_path_list[dem_productions_index]
    # #                     elif 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
    # #                         print(f'已经找到{dem_type}的Reclassify文件,等级{bin_item}.')
    # #                         raster_reclassify_path = srtm_path_list[dem_productions_index]
    # #             else:
    # #                 print('dem_type存在错误，请检查基准DEM的命名。')
    # #
    # #             print(f"当前文件路径:\n"
    # #                   f"输出路径:{xgboost_output_path}\n"
    # #                   f"Slope:{raster_slope_path}\n"
    # #                   f"Aspect:{raster_aspect_path}\n"
    # #                   f"Undulation:{raster_undulation_path}\n"
    # #                   f"Reclassify:{raster_reclassify_path}\n"
    # #                   f"ProjX:{raster_projx_path}\n"
    # #                   f"ProjY:{raster_projy_path}\n")
    # #             # 开始执行预测
    # #             IntegrationXGBoostRegression(point_path,
    # #                                          ['Slope', 'Aspect', 'Undulation', 'Proj_X', 'Proj_Y'],
    # #                                          ['Delta_Ele'],
    # #                                          bin_level,
    # #                                          _output_folder=xgboost_output_path,
    # #                                          _raster_slope_path=raster_slope_path,
    # #                                          _raster_undulation_path=raster_undulation_path,
    # #                                          _raster_aspect_path=raster_aspect_path,
    # #                                          _raster_reclassify_path=raster_reclassify_path,
    # #                                          _raster_projx_path=raster_projx_path,
    # #                                          _raster_projy_path=raster_projy_path)
    # # """
    # # PART 2
    # # """
    # # # 融合
    # # dem_type_list = ['NASA', 'SRTM']
    # # years_list = [i for i in range(2019, 2023)]
    # # bin_list = [i * 50 for i in range(1, 5)]
    # # merge_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\1_PredictData\2_MergeData'
    # # for dem_index, dem_item in enumerate(dem_type_list):
    # #     for year_index, year_item in enumerate(years_list):
    # #         for bin_index, bin_item in enumerate(bin_list):
    # #             predict_folder = os.path.join(xgboost_output_folder, f'{dem_item}_{year_item}_Bin_{bin_item}')
    # #             raster_reclassify_path = None
    # #             if dem_item == 'NASA':
    # #                 print('正在寻找NASA的相关DEM产品路径...')
    # #                 for dem_productions_index, dem_productions_item in enumerate(nasa_files_list):
    # #                     if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
    # #                         print(f'已经找到{dem_type}的Reclassify文件,等级{bin_item}.')
    # #                         raster_reclassify_path = nasa_path_list[dem_productions_index]
    # #             elif dem_item == 'SRTM':
    # #                 print('正在寻找SRTM的相关DEM产品路径...')
    # #                 for dem_productions_index, dem_productions_item in enumerate(srtm_files_list):
    # #                     if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
    # #                         print(f'已经找到{dem_type}的Reclassify文件,等级{bin_item}.')
    # #                         raster_reclassify_path = srtm_path_list[dem_productions_index]
    # #
    # #             MergeRegressionClassify(predict_folder, raster_reclassify_path, merge_output_folder, _dem_type=dem_item,
    # #                                     _year=year_item)
    # """
    # PART 3
    # """
    # # 分析Point位置的Error
    # merge_output_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\1_PredictData\2_MergeData'
    # output_error_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\2_CSVData\1_ErrorCSV'
    # output_mask_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\1_PredictData\3_MaskData'
    # output_change_csv_folder = r'E:\Glacier_DEM_Register\Tanggula_FourYear_Data\Test_20231004\2_CSVData\2_ChangeCSV'
    # merge_predict_paths, merge_predict_files_list = PGFiles.PathGetFiles(merge_output_folder, '.tif')
    # dem_type_list = ['NASA', 'SRTM']
    # years_list = [i for i in range(2019, 2023)]
    # bin_list = [i * 50 for i in range(1, 5)]
    # point_path, merge_predict_path, raster_reclassify_path = None, None, None
    # for dem_index, dem_item in enumerate(dem_type_list):
    #     for year_index, year_item in enumerate(years_list):
    #         for bin_index, bin_item in enumerate(bin_list):
    #             # 寻找Point File Path
    #             if dem_item == 'NASA':
    #                 print('正在执行NASA部分...')
    #                 # 找到对应的point_path
    #                 for point_files_index, point_files_item in enumerate(nasa_point_files_list):
    #                     if dem_item in point_files_item and str(
    #                             year_item) in point_files_item and f'Bin_{bin_item}' in point_files_item:
    #                         print(f'当前执行条件为:{dem_item} {year_item} {bin_item}'
    #                               f'已找到文件名为:{point_files_item}')
    #                         point_path = nasa_point_path_list[point_files_index]
    #                         break
    #                     else:
    #                         print(f'ERROR: 不存在符合条件为:{dem_item} {year_item} {bin_item}的Point Shape文件.')
    #                 for dem_productions_index, dem_productions_item in enumerate(nasa_files_list):
    #                     if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
    #                         print(f'已经找到{dem_item}的Reclassify文件,等级{bin_item}.')
    #                         raster_reclassify_path = nasa_path_list[dem_productions_index]
    #                 for merge_predict_index, merge_predict_item in enumerate(merge_predict_files_list):
    #                     if dem_item in merge_predict_item and str(
    #                             year_item) in merge_predict_item and f'_{bin_item}' in merge_predict_item:
    #                         print(f'已经找到{dem_item}的Merge文件,等级{bin_item}.')
    #                         merge_predict_path = merge_predict_paths[merge_predict_index]
    #             elif dem_item == 'SRTM':
    #                 print('正在执行SRTM部分...')
    #                 # 找到对应的point_path
    #                 for point_files_index, point_files_item in enumerate(srtm_point_files_list):
    #                     if dem_item in point_files_item and str(
    #                             year_item) in point_files_item and f'Bin_{bin_item}' in point_files_item:
    #                         print(f'当前执行条件为:{dem_item} {year_item} {bin_item}'
    #                               f'已找到文件名为:{point_files_item}')
    #                         point_path = srtm_point_path_list[point_files_index]
    #                         break
    #                     else:
    #                         print(f'ERROR: 不存在符合条件为:{dem_item} {year_item} {bin_item}的Point Shape文件.')
    #                 for dem_productions_index, dem_productions_item in enumerate(srtm_files_list):
    #                     if 'Reclassify' in dem_productions_item and f'_{bin_item}' in dem_productions_item:
    #                         print(f'已经找到{dem_item}的Reclassify文件,等级{bin_item}.')
    #                         raster_reclassify_path = srtm_path_list[dem_productions_index]
    #                 for merge_predict_index, merge_predict_item in enumerate(merge_predict_files_list):
    #                     if dem_item in merge_predict_item and str(
    #                             year_item) in merge_predict_item and f'_{bin_item}' in merge_predict_item:
    #                         print(f'已经找到{dem_item}的Merge文件,等级{bin_item}.')
    #                         merge_predict_path = merge_predict_paths[merge_predict_index]
    #             else:
    #                 print('dem_type存在错误，请检查基准DEM的命名。')
    #
    #             csv_output_path = os.path.join(output_error_csv_folder,
    #                                            f'ErrorAnalysis_{dem_item}_{year_item}_Bin_{bin_item}')
    #             AnalysisResult(point_path, merge_predict_path, raster_reclassify_path, f'Bin_{bin_item}', year_item,
    #                            _output_csv_folder=csv_output_path)
    #
    #             output_mask_path = os.path.join(output_mask_folder, f'Mask_{dem_item}_{year_item}_Bin_{bin_item}')
    #             MaskRegionAnalysis(rgi_path, merge_predict_path, output_mask_path, raster_reclassify_path,
    #                                _dem_type=dem_item,
    #                                _bin_level=f'Bin_{bin_item}', _year=year_item,
    #                                _output_csv_folder=output_change_csv_folder, _threshold=30)
    #
    # """
    # PART 4
    # """
