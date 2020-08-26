import numpy as np
import pandas as pd
import xlrd
import xlwt
import joblib
from sklearn.preprocessing import StandardScaler
import numpy as np


def excel_to_matrix(path):
    poly_svr = joblib.load("model.m")
    rows = 0
    cols = 0
    for table in xlrd.open_workbook(path).sheets():
        rows += table.nrows - 1
        cols = table.ncols
    datamatrix = np.zeros((rows, cols))

    for table in xlrd.open_workbook(path).sheets():
        names = xlrd.open_workbook(path).sheet_names()
        counter = 0
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
        ss_x = StandardScaler()
        x = ss_x.fit_transform(datamatrix[:,0:8])
        # 预测 保存预测结果
        poly_svr_y_predict = poly_svr.predict(x)
        poly_svr_y_predict = poly_svr_y_predict * 1.33333333 + 8.0
        sum = 0
        for u in range(row):
            sum += poly_svr_y_predict[u]
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet("Result")
        worksheet.write(counter,0,names[counter])
        worksheet.write(counter,1,sum/row)
    workbook.save("Result.xls")
    print("处理完毕")
    print(datamatrix,cols)
    return datamatrix,cols



datafile = "emotion.xls"
[matrix,col] = excel_to_matrix(datafile)
# print(col)
# x = matrix[:,0:col-2]
# # 1 准备数据
# # 读取波士顿地区房价信息
#
#
# # 2 分割训练数据和测试数据
# # 随机采样25%作为测试 75%作为训练
#
# # 3 训练数据和测试数据进行标准化处理
# ss_x = StandardScaler()
# x = ss_x.fit_transform(x)
#
# ss_y = StandardScaler()
# poly_svr = joblib.load("model.m")
# # 预测 保存预测结果
# poly_svr_y_predict = poly_svr.predict(x)
# poly_svr_y_predict = poly_svr_y_predict*1.33333333 + 8.0
# print(poly_svr_y_predict)


