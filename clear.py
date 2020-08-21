# #https://www.cnblogs.com/supershuai/p/12436669.html
import cv2
import numpy as np
import sys

# 伽玛变换  power函数实现幂函数

if __name__ == "__main__":
    img = cv2.imread("img/image.png", cv2.IMREAD_GRAYSCALE)
    # 归1
    Cimg = img / 255
    # 伽玛变换
    gamma = 0.5
    O = np.power(Cimg,gamma)
    #效果
    cv2.imshow('img',img)
    cv2.imshow('O',O)
    # img.save('img2/test0.png')
    # O.save('img2/test1.png')
    cv2.waitKey(0)
    cv2.destroyAllWindows()



# import cv2
# import numpy as np
# import sys
# from enhance.GrayHist import mget
# if __name__=="__main__":
#     img = cv2.imread("img/image.png",cv2.IMREAD_GRAYSCALE)
#     #求出img 的最大最小值
#     Maximg = np.max(img)
#     Minimg = np.min(img)
#     print(Maximg, Minimg, '-----------')
#     #输出最小灰度级和最大灰度级
#     Omin,Omax = 0,255
#     #求 a, b
#     a = float(Omax - Omin)/(Maximg - Minimg)
#     b = Omin - a*Minimg
#     print(a,b,'-----------')
#     #线性变换
#     O = a*img + b
#     O = O.astype(np.uint8)
#     #利用灰度直方图进行比较  mget为GrayHist中的写方法
#     mget(img)
#     mget(O)
#
#
#     cv2.imshow('img',img)
#     cv2.imshow('enhance',O)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()