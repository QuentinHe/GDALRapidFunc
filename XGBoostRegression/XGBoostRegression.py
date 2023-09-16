# -*- coding: utf-8 -*-
# !/usr/bin/mgdal_env
# @Time : 2023/8/28 14:44
# @Author : Hexk
import os
import warnings

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor

from ReadRasterAndShape import ReadRaster
from ReadRasterAndShape import ReadShape2DataFrame

warnings.filterwarnings("ignore")


def Adjust_Parameters():
    params = {
        'max_depth': [8, 10, 12],  # 每一棵树最大深度，默认6；
        'learning_rate': [0.1, 0.15, 0.3],  # 学习率，每棵树的预测结果都要乘以这个学习率，默认0.3；
        'n_estimators': [450, 600, 800],  # 使用多少棵树来拟合，也可以理解为多少次迭代。默认100；
        # 'objective': ['reg:squarederror'],  # 此默认参数与 XGBClassifier 不同
        'booster': ['gbtree'],
        # 有两种模型可以选择gbtree和gblinear。gbtree使用基于树的模型进行提升计算，gblinear使用线性模型进行提升计算。默认为gbtree
        'gamma': [0.5],  # 叶节点上进行进一步分裂所需的最小"损失减少"。默认0；
        'min_child_weight': [1],  # 可以理解为叶子节点最小样本数，默认1；
        # 'subsample': 0.8,  # 训练集抽样比例，每次拟合一棵树之前，都会进行该抽样步骤。默认1，取值范围(0, 1]
        # 'colsample_bytree': 0.8,  # 每次拟合一棵树之前，决定使用多少个特征，参数默认1，取值范围(0, 1]。
        'reg_alpha': [0],  # 默认为0，控制模型复杂程度的权重值的 L1 正则项参数，参数值越大，模型越不容易过拟合。
        'reg_lambda': [1],  # 默认为1，控制模型复杂度的权重值的L2正则化项参数，参数越大，模型越不容易过拟合。
        'random_state': [0],  # 随机种子
        # 'seed': 123
    }
    other_params = {'subsample': 0.8, 'colsample_bytree': 0.8, 'seed': 123}
    model_adj = XGBRegressor(**other_params)
    optimized_param = GridSearchCV(estimator=model_adj, param_grid=params, scoring='r2', cv=5, verbose=1)
    optimized_param.fit(x_train, y_train)
    # 对应参数的k折交叉验证平均得分
    means = optimized_param.cv_results_['mean_test_score']
    params = optimized_param.cv_results_['params']
    for mean, param in zip(means, params):
        print("mean_score: %f,  params: %r" % (mean, param))
    # 最佳模型参数
    print('参数的最佳取值：{0}'.format(optimized_param.best_params_))
    # 最佳参数模型得分
    print('最佳模型得分:{0}'.format(optimized_param.best_score_))

    # def XGBoostRegressionPredict(self, x_predict_data):
    #     """
    #
    #     :param x_predict_data:  需要预测的全部x数据集，用dict创建，转换为DataFrame格式
    #     :return:    预测的结果，未进行reshape，当写入成Raster需要.reshape(x,y)
    #     """
    #     y_predict = self.model.predict(x_predict_data)
    #     return y_predict


def XGBoostRegression(_x_train, _y_train, _x_validate, _y_validate, _refine_data):
    """
    回归拟合
    :param _x_train: 训练数据
    :param _y_train: 训练数据结果
    :param _x_validate: 验证数据
    :param _y_validate: 验证数据结果
    :param _refine_data:  需要预测的数据
    :return: 预测结果，未降维
    """
    """
    去你妈的。
    拟合过程不可知。
    logloss不适合。
    过拟合不知。
    RMSE有所降低。
    去你妈的。
    """
    print('XGBOOST开始拟合'.center(20, '-'))
    model = xgb.XGBRegressor(max_depth=6,  # 每一棵树最大深度，默认6；
                             learning_rate=0.1,  # 学习率，每棵树的预测结果都要乘以这个学习率，默认0.3；
                             n_estimators=600,  # 使用多少棵树来拟合，也可以理解为多少次迭代。默认100；
                             objective='reg:squarederror',  # 此默认参数与 XGBClassifier 不同
                             booster='gbtree',
                             # 有两种模型可以选择gbtree和gblinear。gbtree使用基于树的模型进行提升计算，gblinear使用线性模型进行提升计算。默认为gbtree
                             gamma=0.5,  # 叶节点上进行进一步分裂所需的最小"损失减少"。默认0；
                             min_child_weight=1,  # 可以理解为叶子节点最小样本数，默认1；
                             subsample=1,  # 训练集抽样比例，每次拟合一棵树之前，都会进行该抽样步骤。默认1，取值范围(0, 1]
                             colsample_bytree=1,  # 每次拟合一棵树之前，决定使用多少个特征，参数默认1，取值范围(0, 1]。
                             reg_alpha=0,  # 默认为0，控制模型复杂程度的权重值的 L1 正则项参数，参数值越大，模型越不容易过拟合。
                             reg_lambda=1,  # 默认为1，控制模型复杂度的权重值的L2正则化项参数，参数越大，模型越不容易过拟合。
                             random_state=0
                             )
    eval_set = [(_x_train, _y_train), (_x_validate, _y_validate)]
    model.fit(_x_train, _y_train, verbose=True, eval_metric=['rmse'], eval_set=eval_set)
    print('XGBOOST拟合完成，开始预测结果'.center(20, '-'))
    y_pred = model.predict(_x_validate)
    print('模型效果评估'.center(20, '-'))

    # 计算其他指标
    r2 = r2_score(_y_validate, y_pred)
    print(f'验证集与预测值的R2 SCORE:{r2}.')
    mse = mean_squared_error(_y_validate, y_pred)
    print(f'验证集与预测值的MSE:{mse},RMSE:{np.sqrt(mse)}')

    print('开始炼丹'.center(20, '-'))
    _predict_data = model.predict(_refine_data)
    print(f'炼制结果长度为:{len(_predict_data)},未降维.')
    return _predict_data


if __name__ == '__main__':
    dir_path = r'E:\Glacier_DEM_Register\Tanggula_ICESat2\10_XGBoost_Data'
    files = os.listdir(dir_path)
    tif_files_list = []
    shp_files_list = []
    for file in files:
        if os.path.splitext(file)[1] == '.tif':
            tif_files_list.append(file)
        elif os.path.splitext(file)[1] == '.shp':
            shp_files_list.append(file)
    nasa_files_list = []
    for item in tif_files_list:
        if 'NASA' in item:
            nasa_files_list.append(item)
    print(nasa_files_list)
    # 读取ATL06_75.shp
    ATL06_75 = ReadShape2DataFrame.ReadPoint2DataFrame(os.path.join(dir_path, '8_ATL06_75.shp'))
    # 得到ATL06_75的DataFrame格式
    ATL06_75_feature_df = ATL06_75.ReadShapeFile()
    ATL06_75_feature_df = ReadShape2DataFrame.DataFrameFormatConvert(ATL06_75_feature_df,
                                                                     int_field=['Segment_ID', 'NASA_Level',
                                                                                'SRTM_Level'],
                                                                     float_field=['Latitudes', 'Longitudes', 'H_Li',
                                                                                  'DEM_H', 'Delta_H', 'NASADEM',
                                                                                  'Delta_NASA',
                                                                                  'SRTMDEM', 'Delta_SRTM'])
    # 读取ATL06_25.shp
    ATL06_25 = ReadShape2DataFrame.ReadPoint2DataFrame(os.path.join(dir_path, '8_ATL06_25.shp'))
    ATL06_25_feature_df = ATL06_25.ReadShapeFile()
    ATL06_25_feature_df = ReadShape2DataFrame.DataFrameFormatConvert(ATL06_25_feature_df,
                                                                     int_field=['Segment_ID', 'NASA_Level',
                                                                                'SRTM_Level'],
                                                                     float_field=['Latitudes', 'Longitudes', 'H_Li',
                                                                                  'DEM_H', 'Delta_H', 'NASADEM',
                                                                                  'Delta_NASA',
                                                                                  'SRTMDEM', 'Delta_SRTM'])
    # 得到5个训练参数的未降数组
    nasadem_ds = ReadRaster.ReadRaster(os.path.join(dir_path, '10_NASADEM.tif'))
    nasadem_data = nasadem_ds.ReadRasterFile()
    nasa_undulation_ds = ReadRaster.ReadRaster(os.path.join(dir_path, '10_NASA_Undulation.tif'))
    nasa_undulation_data = nasa_undulation_ds.ReadRasterFile()
    nasa_bin_level_ds = ReadRaster.ReadRaster(os.path.join(dir_path, '10_Tanggula_NASADEM_Reclassify.tif'))
    nasa_bin_level_data = nasa_bin_level_ds.ReadRasterFile()
    nasa_aspect_ds = ReadRaster.ReadRaster(os.path.join(dir_path, '10_NASADEM_Aspect.tif'))
    nasa_aspect_data = nasa_aspect_ds.ReadRasterFile()
    nasa_slope_ds = ReadRaster.ReadRaster(os.path.join(dir_path, '10_NASADEM_Slope.tif'))
    nasa_slope_data = nasa_slope_ds.ReadRasterFile()
    # 获取75和25的行列位置
    point_row_train, point_column_train = ATL06_75.PointMatchRasterRowColumn(nasadem_ds.raster_ds_geotrans)
    point_row_validate, point_column_validate = ATL06_25.PointMatchRasterRowColumn(nasadem_ds.raster_ds_geotrans)
    # 获取点位置对应的栅格值
    # 75 Train
    point_nasadem_train = ReadRaster.SearchRasterRowColumnData(nasadem_data, point_row_train, point_column_train)
    point_nasa_undulation_train = ReadRaster.SearchRasterRowColumnData(nasa_undulation_data, point_row_train,
                                                                       point_column_train)
    point_nasa_bin_level_train = ReadRaster.SearchRasterRowColumnData(nasa_bin_level_data, point_row_train,

                                                                      point_column_train)

    point_nasa_aspect_train = ReadRaster.SearchRasterRowColumnData(nasa_aspect_data, point_row_train,

                                                                   point_column_train)

    point_nasa_aspect_level_train = ReadShape2DataFrame.AspectConvertLevel(point_nasa_aspect_train)
    point_nasa_slope_train = ReadRaster.SearchRasterRowColumnData(nasa_slope_data, point_row_train, point_column_train)
    # 25 Validate
    point_nasadem_validate = ReadRaster.SearchRasterRowColumnData(nasadem_data, point_row_validate,
                                                                  point_column_validate)
    point_nasa_undulation_validate = ReadRaster.SearchRasterRowColumnData(nasa_undulation_data, point_row_validate,
                                                                          point_column_validate)
    point_nasa_bin_level_validate = ReadRaster.SearchRasterRowColumnData(nasa_bin_level_data, point_row_validate,
                                                                         point_column_validate)
    point_nasa_aspect_validate = ReadRaster.SearchRasterRowColumnData(nasa_aspect_data, point_row_validate,
                                                                      point_column_validate)
    point_nasa_aspect_level_validate = ReadShape2DataFrame.AspectConvertLevel(point_nasa_aspect_validate)
    point_nasa_slope_validate = ReadRaster.SearchRasterRowColumnData(nasa_slope_data, point_row_validate,
                                                                     point_column_validate)
    # 生成训练数据
    # 原始数据组
    """
    原始训练数据：经度、纬度、起伏度、高程箱等级、坡向箱等级、坡度、基准DEM
        训练结果：H_Li真实值；
    """
    x_train_dict = dict(
        Latitudes=ATL06_75_feature_df['Latitudes'],
        Longitudes=ATL06_75_feature_df['Longitudes'],
        Undulation=point_nasa_undulation_train,
        NASA_Level=point_nasa_bin_level_train,
        Aspect_Level=point_nasa_aspect_level_train,
        Slope=point_nasa_slope_train,
        DEM=point_nasadem_train
    )
    x_train = pd.DataFrame(x_train_dict)
    y_train_dict = dict(
        H_Li=ATL06_75_feature_df['H_Li']
    )
    y_train = pd.DataFrame(y_train_dict)
    x_validate_dict = dict(
        Latitudes=ATL06_25_feature_df['Latitudes'],
        Longitudes=ATL06_25_feature_df['Longitudes'],
        Undulation=point_nasa_undulation_validate,
        NASA_Level=point_nasa_bin_level_validate,
        Aspect_Level=point_nasa_aspect_level_validate,
        Slope=point_nasa_slope_validate,
        DEM=point_nasadem_validate
    )
    # for i in x_train_dict:
    #     print(len(i))
    x_validate = pd.DataFrame(x_validate_dict)
    y_validate_dict = dict(
        H_Li=ATL06_25_feature_df['H_Li']
    )
    y_validate = pd.DataFrame(y_validate_dict)
    XGBoostRegression(x_train, y_train, x_validate, y_validate)
