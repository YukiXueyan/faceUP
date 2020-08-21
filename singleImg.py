import http.client
import json
import ssl
import urllib.parse
import os
from os.path import expanduser

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


img = open(expanduser('D:/1_study/2.0work/faceUP/img/16.jpg'), "rb")
# img = open(expanduser('D:/1_study/2.0work/faceUP/img/image.png'), "rb")

try:
    conn = http.client.HTTPSConnection('api.cognitive.azure.cn')
    conn.request("POST", "/face/v1.0/detect?%s" % params, img, headers)
    response = conn.getresponse()
    data = response.read()
    parsed = json.loads(data)  # 将字符串转化为字典
    print("Response:")
    print(json.dumps(parsed, sort_keys=True, indent=2))
    word = json.dumps(parsed, sort_keys=True, indent=2)
    print("len:", len(word))
    with open("result/test16_0.txt", "w") as f:
        f.write("原图测试：")
        f.write(json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

