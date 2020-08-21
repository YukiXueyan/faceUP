import http.client
import json
import os,sys
import ssl
import urllib
import urllib.parse
import xlwt
import time
from PIL import ImageEnhance
# 新添加
import cv2
from PIL import Image

ssl._create_default_https_context = ssl._create_unverified_context
# urllib打开http链接会验证SSL证书，全局取消证书验证防止异常
subscription_key = '144ce86219b740938b003a1f3d36a26a'  # Face API的key
uri_base = 'https://aimovie.cognitiveservices.azure.cn/'  # Face API的end point
#path = '/Users/mac/Documents/filmRating/newPicture' #新电影的处理后图片
path = 'img'
def useApi(img):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,smile,emotion'
    })
    try:
        conn = http.client.HTTPSConnection('api.cognitive.azure.cn')
        conn.request("POST", "/face/v1.0/detect?%s" % params, img, headers)
        response = conn.getresponse()
        data = response.read()
        parsed = json.loads(data)  # 将字符串转化为字典
        #print("Response:")
        #print(json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return parsed


workbook = xlwt.Workbook(encoding='utf-8')

def writeExcel(img, worksheet, row, file_name, path, file_num):
    parsedAll = []
    parse = useApi(img)
    if len(parse) == 0:
        print("未识别到人脸，正在进行第一次加工")
        img = changePhoto(img,1.5,2.0) #未识别到人脸，第一次加工
        parse = useApi(img)
        if len(parse) == 0:
            print("未识别到人脸，正在进行第二次加工")
            img = changePhoto(img,0.9,2.0) #仍未识别到人脸，第二次加工
            parse = useApi(img)
            if len(parse) == 0:
                print('无法识别到人脸')

    parsedAll.append(parse)
    if len(parse) != 0:
        for list_item in parsedAll:
            if type(list_item) == list:  # 正确的输出结果应被转化为list类型
                l1 = list_item[0]  # list_item里只有一个元素l1，l1是一个字典
                filename, extension = os.path.splitext(file_name)
                worksheet.write(row, 0, filename)  # 写入照片的文件名

                times = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                worksheet.write(row, 1, times)  # 写入时间戳

                emotion = []
                for k in l1.keys():  # l1的key值分别为faceAttributes，faceId，faceRectangle
                    if k == 'faceAttributes':
                        l2 = l1[k]  # faceAttributes的value是一个字典,赋值给l2
                        worksheet.write(row, 2, l2['gender'])  # 性别写进第3列
                        worksheet.write(row, 3, l2['age'])  # age写进第4列

                        l3 = l2['emotion']  # emotion的value是一个字典，赋值给l3
                        for emotion_k in l3.keys():
                            emotion.append(l3[emotion_k])  # 把所有情绪识别分数存入emotion数组

                        max_emotion = 0
                        for i in range(len(emotion)):
                            worksheet.write(row, 4 + i, str(emotion[i]))
                            if emotion[i] > max_emotion:
                                max_emotion = emotion[i]  # 获取得分最高的情绪

                        for i in range(len(emotion)):
                            if max_emotion == emotion[i]:
                                worksheet.write(row, 12, str(i))  # 记录得分最高的情绪编号
                                # 0-anger,1-contempt,2-disgust,3-fear,4-happiness,5-neutral,6-sadness,7-surprise

                    elif k == 'faceId':
                        worksheet.write(row, 13, l1['faceId'])  # faceId写进第14列
                    else:
                        pass

                print('图片:' + str(file_name) + '已处理完毕')
            else:
                pass
                row += 1

    return row, worksheet

def changePhoto(img,bri,sharp):
   print('img的type:')
   print(type(img))
   im_2 = ImageEnhance.Brightness(img).enhance(bri)
   im_3 = ImageEnhance.Sharpness(im_2).enhance(sharp)
   print("加工完毕！")
   return im_3

for root, dirs, files in os.walk(path, topdown=False):
    # 创建生成器，查找目录及子目录下所有文件,root-文件夹路径，dirs-文件夹名字，files-文件名
    for folder in dirs:
        error_num = 0
        error_list = []
        row = 0
        file_num = 0
        print('现在开始处理文件夹：' + folder)
        worksheet = workbook.add_sheet(folder)

        title = ['PhotoID', 'Time', 'gender', 'age', 'anger', 'contempt', 'disgust',
                 'fear', 'happiness', 'neutral', 'sadness', 'surprise', 'emotion', 'faceID']  # 设置表头

        for col in range(len(title)):
            worksheet.write(0, col, title[col])
        for root2, dirs2, files2 in os.walk(path + '/' + folder):
            for file_name in files2:
                try:
                    path2 = path + '/' + folder + '/' + file_name
                    print('现在处理' + folder + '中的图片:' + str(file_name))
                    img = open(os.path.expanduser(path2), 'rb')  # 打开本地图片
                    row, worksheet = writeExcel(img, worksheet, row, file_name, path2, file_num)
                    file_num += 1
                except Exception as e:
                    print(e)
        print('文件夹：' + folder + '已处理完毕')
        print(error_num, error_list)  # 异常个数、异常内容

workbook.save('Face.xls')#没有打分的新电影的情绪分
print('处理完毕')
