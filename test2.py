import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


# 绘制直方图函数
def grayHist(img):
    h, w = img.shape[:2]
    pixelSequence = img.reshape([h * w, ])
    numberBins = 256
    histogram, bins, patch = plt.hist(pixelSequence, numberBins,
                                      facecolor='black', histtype='bar')
    plt.xlabel("gray label")
    plt.ylabel("number of pixels")
    plt.axis([0, 255, 0, np.max(histogram)])
    plt.show()


# img = cv.imread("../testImages/4/img4.jpg", 0)
# out = 2.0 * img
# # 进行数据截断，大于255的值截断为255
# out[out > 255] = 255
# # 数据类型转换
# out = np.around(out)
# out = out.astype(np.uint8)
# # 分别绘制处理前后的直方图
# # grayHist(img)
# # grayHist(out)
# cv.imshow("img", img)
# cv.imshow("out", out)
# cv.waitKey()

img = cv.imread("img/image.png", 0)
img = cv.resize(img, None, fx=0.3, fy=0.3)
h, w = img.shape[:2]
out = np.zeros(img.shape, np.uint8)
for i in range(h):
    for j in range(w):
        pix = img[i][j]
        if pix < 50:
            out[i][j] = 0.5 * pix
        elif pix < 150:
            out[i][j] = 3.6 * pix - 310
        else:
            out[i][j] = 0.238 * pix + 194
        # 数据类型转换
out = np.around(out)
out = out.astype(np.uint8)
# grayHist(img)
# grayHist(out)
cv.imshow("img", img)
cv.imshow("out", out)
cv.waitKey()