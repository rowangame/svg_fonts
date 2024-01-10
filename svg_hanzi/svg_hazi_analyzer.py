# -*- coding:utf-8 -*-
import json
import os

from selenium import webdriver
from selenium.webdriver import ChromeOptions
import cv2
import numpy as np

import imageio

character_cell_dict_path = "./hanzi-data/character-cell-dict.txt"
svg_origin_path_fmt = "./hanzi-data/svgs/%d.svg"
out_png_dir_fmt = "./hanzi-data/out-pngs/%d.png"
out_png_tmp = "./hanzi-data-1/out-pngs/temp.png"
out_gifs_dir_fmt = "./hanzi-data/out-gifs/%d"

character_dict = []

# 加载数据描述字典数据
def loadCharacterCellDict():
    with open(character_cell_dict_path, encoding="utf-8") as f:
        for line in f.readlines():
            if not line:
                continue
            data = json.loads(line.strip())
            character_dict.append(data)
        print("len(character)=%d" % len(character_dict))

# 用Chrome浏览器引擎加载svg文件(显示图像并保存到文件中)
# 也可以用其它方式解析svg文件
def loadSvgFileByChrome():
    try:
        print("初始化Chrome")
        opt = ChromeOptions()  # 创建Chrome参数对象
        opt.add_argument('--headless')

        # 创建浏览器对象
        driver = webdriver.Chrome(options=opt)  # 使用Chrome驱动
        driver.set_window_size(1024, 1024)

        total_size = len(character_dict)
        for i in range(total_size):
            tmpData = character_dict[i]

            tmpCode = tmpData['code']
            print("i=%d tmpCode=%d" % (i + 1, tmpCode))
            uri = "file:///E:/python/base_demo/matplotlib/svg_demo/svg_hanzi/hanzi-data-1/svgs/%d.svg" % tmpCode
            # 打开网页(本地文件)
            driver.get(uri)

            # 等待页面加载完成(等待5秒钟,可以根据实际情况调整等待时间)
            driver.implicitly_wait(5)

            # 获取页面截图(截图保存路径)
            # screenshot_path = out_png_dir_fmt % tmpCode
            # driver.save_screenshot(screenshot_path)

            # 修改为从内存数据加载图像数据
            # 转化为bytes数据
            tmpBuffer = driver.get_screenshot_as_png()
            # 转化为一维数组
            tmpArray = np.frombuffer(tmpBuffer, np.uint8)
            # 从数组中解析图像
            tmpImg = cv2.imdecode(tmpArray, cv2.IMREAD_ANYCOLOR)
            # cv2.imwrite(out_png_dir_fmt % tmpCode, imgCv)
            # 解析数据到每个子区域,并保存到文件
            print("解析数据到每个子区域,并保存到文件,tmpCode=%d" % tmpCode)
            splitStrokes(tmpImg, tmpData)

            # 生成gif图片
            print("生成gif图片,tmpCode=%d" % tmpCode)
            srcDir = out_gifs_dir_fmt % tmpCode
            strokesToGif(srcDir, tmpData)

            # 测试前几项
            if i > 5: break
        # 关闭浏览器
        print("退出中...")
        driver.quit()
        print("退出成功")
    except Exception as e:
        print(repr(e))

# 解析数据到每个子区域,并保存到文件
def splitStrokes(srcData, characterData):
    imgSrc = srcData

    # 先生成子目录
    tmpCode = characterData['code']
    subdir = out_gifs_dir_fmt % tmpCode
    if not os.path.exists(subdir):
        os.mkdir(subdir)

    # 区域宽度和高度
    width = 128
    height = 128
    # 第一行最多显示的区域
    per_lines = 6
    # 总笔画数
    count = characterData['strokes']

    # 分析每一个区域数据
    for i in range(count):
        tmpImg = np.zeros((height, width, imgSrc.shape[2]), np.uint8)

        curStroke = i + 1
        if curStroke % per_lines == 0:
            # 向下取整计算(下标值从0开始)
            tmpRow = curStroke // per_lines - 1
            tmpCol = per_lines - 1
        else:
            # 向下取整计算(下标值从0开始)
            tmpRow = curStroke // per_lines
            tmpCol = curStroke % per_lines - 1
        # 复制每一个区域的图像数据
        tmpImg[0:height, 0:width] = imgSrc[tmpRow * height: (tmpRow + 1) * height, tmpCol * width: (tmpCol + 1) * width]
        fileName = subdir + "/%d-%02d.png" % (tmpCode, i)
        # print(fileName)
        cv2.imwrite(fileName, tmpImg)

# 生成gif图片
def strokesToGif(srcDir, characterData):
    # 记录原来的路径
    oridir = os.getcwd()
    try:
        # 改变当前工作目录到指定的路径
        os.chdir(srcDir)
        # 这里加载后,会按字母顺序排序(需要重新按数字值排序一下,否则gif图片动画显示错误)
        # 文件夹中的文件/文件夹的名字列表
        file_list = os.listdir()
        # 读入缓冲区
        frames = []
        for tmpPng in file_list:
            if tmpPng.endswith(".png"):
                frames.append(imageio.v2.imread(tmpPng))
        gifname = "%d.gif" % characterData['code']
        # total_time = 5000
        # dtime = total_time / characterData['strokes']
        dtime = 350
        imageio.mimsave(gifname, frames, 'GIF', duration=dtime)
    finally:
        # 恢复为原来的路径(不恢复原来的路径,下次生成时,就会出现找不到路径的问题)
        os.chdir(oridir)

# 生成所有汉字字符
def makeAllCharacters():
    loadCharacterCellDict()
    print(len(character_dict))
    print(character_dict[0])
    for i in range(len(character_dict)):
        print("dict(%d):" % i)
        tmpDict = character_dict[i]
        code = tmpDict['code']
        strokes = tmpDict['strokes']
        path = 'hanzi-data-1/out-pngs/%d/%d-%02d.png' % (code, code, strokes - 1)
        img = cv2.imread(path)
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, imgTwo = cv2.threshold(imgGray, 254, 255, cv2.THRESH_BINARY)
        savePath = 'hanzi-data-1/out-all/%d.png' % (code)
        cv2.imwrite(savePath, imgTwo)

# loadCharacterCellDict()
# loadSvgFileByChrome()
makeAllCharacters()