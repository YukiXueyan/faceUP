import cv2
# import opencv
from PIL import Image,ImageFilter
from PIL import ImageEnhance
import matplotlib.image as mp
import os, sys

import http.client
import json
import ssl
import urllib.parse
from os.path import expanduser

#操作名称
Bri=1.5
Sharp=2.0

#获取图片清晰度
def getImageVar(imgPath):
   image = cv2.imread(imgPath);
   img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
   return imageVar

#修改图片亮度和对比度
#修改的值待定
def changePhoto(path,file,bri,sharp):
   im = Image.open(path+file)
   print('im的type:')
   print(type(im))
   # # 亮度
   im_2 = ImageEnhance.Brightness(im).enhance(bri)

   img3 = ImageEnhance.Sharpness(im_2).enhance(sharp)

   img3.save('img2/'+file)


#获取结果
def result(path,file,bri):
   ssl._create_default_https_context = ssl._create_unverified_context
   # urllib打开http链接会验证SSL证书，全局取消证书验证防止异常

   subscription_key = '144ce86219b740938b003a1f3d36a26a'  # Face API的key
   uri_base = 'https://aimovie.cognitiveservices.azure.cn/'  # Face API的end point

   global parsed
   headers = {
      'Content-Type': 'application/octet-stream',
      'Ocp-Apim-Subscription-Key': subscription_key,
   }

   params = urllib.parse.urlencode({
      'returnFaceId': 'true',
      'returnFaceLandmarks': 'false',
      'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
   })  # 返回的内容，FaceID，年龄，性别，头型，微笑，面部毛发，眼镜，情绪，头发，化妆，遮挡，配饰，模糊，曝光，干扰

   # img = open(expanduser('D:/1_study/2.0work/faceUP/img2/16.jpg'), "rb")
   img = open(expanduser(path+file), "rb")

   try:
      conn = http.client.HTTPSConnection('api.cognitive.azure.cn')
      conn.request("POST", "/face/v1.0/detect?%s" % params, img, headers)
      response = conn.getresponse()
      data = response.read()
      parsed = json.loads(data)  # 将字符串转化为字典
      print("Response:")
      print(json.dumps(parsed, sort_keys=True, indent=2))
      word=json.dumps(parsed, sort_keys=True, indent=2)
      # print(path+file)
      # print("len:",len(word))
      with open("result/"+file+".txt", "w") as f:
         f.write(file)
         f.write("Bri:"+str(bri))
         f.write("Sharp:" + str(Sharp))
         f.write(json.dumps(parsed, sort_keys=True, indent=2))
      conn.close()
      return len(word)

   except Exception as e:
      print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == '__main__':
   path1='img/'
   path2='img2/'

#从文件夹中遍历图片
dirs = os.listdir(path1)
for file in dirs:
   # 原图识别
   result(path1, file,1)
   length=result(path1,file,1)
   if length==2:
      # 提高亮度为1.5，锐度为2.0
      changePhoto(path1, file, Bri, Sharp)
      length=result(path2,file,Bri)
      if length == 2:
         # 降低原图亮度为0.9
         changePhoto(path1, file, 0.9, Sharp)
         length = result(path2, file,0.9)
         if length ==2:
            # 照片还是无法识别
            print("照片无法识别")
      else:
         print("end")