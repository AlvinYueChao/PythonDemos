# -*-coding:utf-8 -*-
# @Time: 2022/5/18 14:09
# @Author: zou wei
# @File: boston_pricing_linear_regression.py
# @Contact: visio@163.com
# @Software: PyCharm
import os.path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from time import time
import joblib

if __name__ == "__main__":
    # print(mpl.rcParams)
    mpl.rcParams["font.family"] = "simHei"
    mpl.rcParams["axes.unicode_minus"] = False
    model_filename = "boston_poly_rf.h5"
    MODEL_LOAD = False
    col_names = [
        "CRIM",
        "ZN",
        "INDUS",
        "CHAS",
        "NOX",
        "RM",
        "AGE",
        "DIS",
        "RAD",
        "TAX",
        "PTRATIO",
        "B",
        "LSTAT",
        "MEDV",
    ]
    data = pd.read_csv("housing.data", header=None, sep="\s+", names=col_names)
    print(data)
    # x = data[col_names[:-1]]
    x = data.drop(labels="MEDV", axis=1)
    y = data["MEDV"]
    # print(x, y)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=0
    )

    if MODEL_LOAD and os.path.exists(model_filename):
        print("加载模型...")
        model = joblib.load(model_filename)
    else:
        print("训练模型...")
        # rf = RandomForestRegressor(n_estimators=20)
        # model = GridSearchCV(rf, cv=3, param_grid={
        #     'max_depth': np.arange(2, 14),
        #     'criterion': ['squared_error', 'absolute_error', 'poisson'],
        #     'min_samples_split': np.arange(2, 6)
        # })
        # t_start = time()
        # model.fit(x_train, y_train)
        # print('耗时：%.5f秒' % (time()-t_start))
        # print('最优参数：', model.best_params_)
        # model = model.best_estimator_
        model = Pipeline(
            [
                ("pf", PolynomialFeatures(degree=2, include_bias=False)),
                # ('linear_regression', LinearRegression(fit_intercept=False))
                (
                    "rf",
                    RandomForestRegressor(
                        n_estimators=20,
                        criterion="squared_error",
                        max_depth=7,
                        min_samples_split=3,
                    ),
                ),
            ]
        )
        model.fit(x_train, y_train)
        joblib.dump(model, model_filename)

    # lr = model.get_params()['ridge']
    # print('特征个数：', len(lr.coef_))
    # print(model.coef_)
    # print(model.intercept_)
    # coefficient = pd.DataFrame(data=model.coef_, index=col_names[:-1], columns=['系数'])
    # coefficient.loc['-<INTERCEPT->', '系数'] = model.intercept_
    # print(coefficient)
    # coefficient.sort_values('系数', ascending=False, inplace=True)
    # plt.bar(coefficient.index, coefficient['系数'].values, width=0.5)
    # plt.grid(ls=':', b=True)
    # plt.xlabel('特征', fontsize=12)
    # plt.ylabel('权值', fontsize=12)
    # plt.title('波士顿房价数据中线性回归模型权重', fontsize=15)
    # plt.savefig('boston.png')
    # plt.show()

    y_train_pred = model.predict(x_train)
    mse_train = mean_squared_error(y_train, y_train_pred)
    mae_train = mean_absolute_error(y_train, y_train_pred)
    print("训练数据集：MSE=%.4f，MAE=%.4f" % (mse_train, mae_train))

    y_test_pred = model.predict(x_test)
    mse_test = mean_squared_error(y_test, y_test_pred)
    mae_test = mean_absolute_error(y_test, y_test_pred)
    print("测试数据集：MSE=%.4f，MAE=%.4f" % (mse_test, mae_test))
    # print(np.sqrt(mse)/np.mean(y), mae/np.mean(y))
