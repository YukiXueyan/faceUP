import numpy as np
import pandas as pd
import xlrd
from sklearn import preprocessing, model_selection
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np


def excel_to_matrix(path):
    rows = 0
    cols = 0
    for table in xlrd.open_workbook(path).sheets():
        rows += table.nrows - 1
        cols = table.ncols
    datamatrix = np.zeros((rows, cols))

    for table in xlrd.open_workbook(path).sheets():
        # # table = xlrd.open_workbook(path).sheets()[0]  # 获取第一个sheet表
        row = table.nrows - 1  # 行数
        # print(row)
        col = table.ncols  # 列数
        # datamatrix = np.zeros((row, col))  # 生成一个nrows行ncols列，且元素均为0的初始矩阵
        for y in range(row):
            for x in range(col):
                # 把list转换为矩阵进行矩阵操作
                datamatrix[y, x] = table.row(y + 1)[x].value  # 按列把数据存进矩阵中
        # 数据归一化
        # min_max_scaler = preprocessing.MinMaxScaler()
        # datamatrix = min_max_scaler.fit_transform(datamatrix)
        return datamatrix


datafile = "emotion.xls"
matrix = excel_to_matrix(datafile)

x = matrix[:, 0:8]

y = matrix[:, 9]

# 1 准备数据
# 读取波士顿地区房价信息


# 2 分割训练数据和测试数据
# 随机采样25%作为测试 75%作为训练
x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.25, random_state=33)

# 3 训练数据和测试数据进行标准化处理
ss_x = StandardScaler()
x_train = ss_x.fit_transform(x_train)
x_test = ss_x.transform(x_test)

ss_y = StandardScaler()
y_train = ss_y.fit_transform(y_train.reshape(-1, 1))
y_test = ss_y.transform(y_test.reshape(-1, 1))

print(ss_y.mean_)
print(ss_y.scale_)
# 4.1 支持向量机模型进行学习和预测
# 线性核函数配置支持向量机
linear_svr = SVR(kernel="linear")
# 训练
linear_svr.fit(x_train, np.ravel(y_train))
# 预测 保存预测结果
linear_svr_y_predict = linear_svr.predict(x_test)
# print(y_test)
# # print(linear_svr_y_predict)

# 多项式核函数配置支持向量机
poly_svr = SVR(kernel="poly")
# 训练
poly_svr.fit(x_train, np.ravel(y_train))
# 预测 保存预测结果
poly_svr_y_predict = poly_svr.predict(x_test)

y_test = ss_y.inverse_transform(y_test)
poly_svr_y_predict = ss_y.inverse_transform(poly_svr_y_predict)
print(y_test)
print(poly_svr_y_predict)

# 5 模型评估
# 线性核函数 模型评估
# print("线性核函数支持向量机的默认评估值为：", linear_svr.score(x_test, y_test))
# print("线性核函数支持向量机的R_squared值为：", r2_score(y_test, linear_svr_y_predict))
# print("线性核函数支持向量机的均方误差为:", mean_squared_error(ss_y.inverse_transform(y_test),
#                                               ss_y.inverse_transform(linear_svr_y_predict)))
# print("线性核函数支持向量机的平均绝对误差为:", mean_absolute_error(ss_y.inverse_transform(y_test),
#                                                  ss_y.inverse_transform(linear_svr_y_predict)))
# # 对多项式核函数模型评估
# print("对多项式核函数的默认评估值为：", poly_svr.score(x_test, y_test))
# print("对多项式核函数的R_squared值为：", r2_score(y_test, poly_svr_y_predict))
print("对多项式核函数的均方误差为:", mean_squared_error(y_test,poly_svr_y_predict),str(type(mean_squared_error(y_test,poly_svr_y_predict))))
print("对多项式核函数的平均绝对误差为:", mean_absolute_error(y_test,poly_svr_y_predict))

joblib.dump(poly_svr,"model.m")
print("Done\n")
