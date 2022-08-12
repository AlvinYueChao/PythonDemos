import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    # print(mpl.rcParams)
    mpl.rcParams["font.family"] = "simHei"
    mpl.rcParams["axes.unicode_minus"] = False
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

    model = LinearRegression()
    model.fit(x_train, y_train)
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
