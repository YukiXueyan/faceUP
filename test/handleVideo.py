import os
# 用到了OpenCV
import cv2
# 用到了Pillow
import PIL.Image as img

# 视频源文件路径
videos_src_path = './filmRating/Video'
# 视频分帧图片父级保存路径
videos_save_path = './filmRating/picture'
# 获取视频源文件路径下的所有视频文件
videos = os.listdir(videos_src_path)
# 对各视频进行排序
# videos.sort(key=lambda x: int(x[5:-4]))

i = 1

for each_video in videos:
    # 生成单个视频分帧图片保存路径
    if not os.path.exists(videos_save_path + '/' + str(i)):
        os.mkdir(videos_save_path + '/' + str(i))
    # 视频帧全路径
    each_video_save_full_path = os.path.join(videos_save_path, str(i)) + '/'
    # 视频截取部分帧全路径
    each_video_savePart_full_path = os.path.join(videos_save_path, str(i)+'Part') + '/'
    # 视频全路径
    each_video_full_path = os.path.join(videos_src_path, each_video)
    # 创建一个视频读写类 读入视频文件
    cap = cv2.VideoCapture(each_video_full_path)
    # 初始化第一个帧号
    frame_count = 1
    success = True


    #
    # # 读取视频的fps(帧率),  size(分辨率)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # print("fps: {}\n size: {}".format(fps, size))
    #
    # # 读取视频时长（帧总数）
    # total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # print("[INFO] {} total frames in video".format(total))
    #
    # # 设定从视频的第几帧开始读取
    # # From :  https://blog.csdn.net/luqinwei/article/details/87973472
    # frameToStart = 2000
    # cap.set(cv2.CAP_PROP_POS_FRAMES, frameToStart);
    #

    while (success):
        success, frame = cap.read()
        # 存储为图像
        if success == True:
            cv2.imwrite(each_video_save_full_path + "frame%d.jpg" % frame_count,
                        frame)
#对图片进行区域裁剪的代码块
            IMG = each_video_save_full_path + "frame%d.jpg" % frame_count  # 图片地址
        # 打印图片地址
            print(IMG)
            im = img.open(IMG)  # 用PIL打开一个图片
            box = (0, 0, 318, 360)  # box代表需要剪切图片的位置格式为:xmin ymin xmax ymax
            ng = im.crop(box)  # 对im进行裁剪 保存为ng(这里im保持不变)
            # ng = ng.rotate(20)  # ng为裁剪出来的图片，进行向左旋转20度 向右为负数
        # 创建用于存放裁剪后的图片的文件夹
            if not os.path.exists(each_video_savePart_full_path):
                os.mkdir(each_video_savePart_full_path)
        # 打印裁剪后的图片地址
            partPath = each_video_savePart_full_path + "frame%d.jpg" % frame_count
            print(partPath)
        # 存储裁剪后的图片
            ng.save(each_video_savePart_full_path + "frame%d.jpg" % frame_count)
# 裁剪并保存结束

        #设置分帧间隔(捕获本视频的下一帧)
        frame_count = frame_count + 500
    #处理下一个视频
    i = i + 1

    cap.release()