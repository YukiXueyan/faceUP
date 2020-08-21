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

#获取图片清晰度
def getImageVar(imgPath):
   image = cv2.imread(imgPath);
   img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
   return imageVar

#修改图片亮度和对比度
#修改的值待定
def changePhoto(path,file):
   im = Image.open(path+file)
   # # 亮度
   im_2 = ImageEnhance.Brightness(im).enhance(0.9)
   # # im_2.show()
   # # 提高对比度
   # im_3 = ImageEnhance.Contrast(im_2).enhance(1.0)
   # im_3.show()
   #提高锐度
   enh_sha = ImageEnhance.Sharpness(im_2).enhance(2.0)
   enh_sha.show()
   #文件保存
   # im_3.save('img2/'+file)
   enh_sha.save('img2/'+file)

def main():
   # 打开文件
   # 文件夹
   path = "img/"
   dirs = os.listdir(path)
   i = int(1)
   # 输出所有文件和文件夹
   for file in dirs:
      cl = getImageVar(path + file)
      print(cl)
      # 判断清晰度是否达到要求，对达不到要求的图片进行增加亮度和对比度的操作
      # 清晰度判断值待定
      if cl <= 100:
         changePhoto(path, file)

      # print(getImageVar('img2/'+file))

def result():
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

   img = open(expanduser('D:/1_study/2.0work/faceUP/img2/16.jpg'), "rb")
   # img = open(expanduser('D:/1_study/2.0work/faceUP/img/image.png'), "rb")

   try:
      conn = http.client.HTTPSConnection('api.cognitive.azure.cn')
      conn.request("POST", "/face/v1.0/detect?%s" % params, img, headers)
      response = conn.getresponse()
      data = response.read()
      parsed = json.loads(data)  # 将字符串转化为字典
      print("Response:")
      print(json.dumps(parsed, sort_keys=True, indent=2))
      word=json.dumps(parsed, sort_keys=True, indent=2)
      print("len:",len(word))
      with open("result/test16锐度2.0Bri0.9.txt", "w") as f:
         f.write(json.dumps(parsed, sort_keys=True, indent=2))
      conn.close()

   except Exception as e:
      print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__ == '__main__':
   path='img/'
   file='16.jpg'
   changePhoto(path,file)
   result()

