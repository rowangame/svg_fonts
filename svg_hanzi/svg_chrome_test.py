# -*- coding: utf-8 -*-
import os

from selenium import webdriver
from selenium.webdriver import ChromeOptions
import cv2
import numpy as np

# 浏览器加载方式(注意:文件路径目录)
def testSvg():
    try:
        # 创建浏览器对象
        driver = webdriver.Chrome()  # 使用 Chrome 驱动
        driver.set_window_size(1024, 1024)

        character = '赢'
        code = ord(character)
        # 打开网页(本地文件)
        uri = "file:///E:/python/base_demo/matplotlib/svg_demo/svg_hanzi/hanzi-data-1/svgs/%d.svg" % code
        driver.get(uri)
        # 等待页面加载完成
        driver.implicitly_wait(5)  # 等待 5 秒钟，可以根据实际情况调整等待时间

        # 获取页面截图
        screenshot_path = "./hanzi-data-1/out-test/%d.png" % code  # 截图保存路径
        driver.save_screenshot(screenshot_path)

        # 关闭浏览器
        driver.quit()
    except Exception as e:
        print(repr(e))

# 以隐藏浏览器的方式加载(svg文件)
def testSvg2():
    try:
        print("初始化Chrome")
        opt = ChromeOptions()  # 创建Chrome参数对象
        opt.add_argument('--headless')

        # opt.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        # opt.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
        # opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        # opt.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
        # opt.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
        # opt.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败

        # 创建浏览器对象
        driver = webdriver.Chrome(options=opt)  # 使用 Chrome 驱动
        driver.set_window_size(1024, 1024)

        print("加载svg文件")
        character = '赢'
        code = ord(character)
        # 打开网页(本地文件)
        uri = "file:///E:/python/base_demo/matplotlib/svg_demo/svg_hanzi/hanzi-data-1/svgs/%d.svg" % code
        driver.get(uri)

        # 等待页面加载完成
        driver.implicitly_wait(5)  # 等待 5 秒钟，可以根据实际情况调整等待时间

        print("截图保存")
        # 获取页面截图
        screenshot_path = "./hanzi-data-1/out-test/%d.png" % code  # 截图保存路径
        driver.save_screenshot(screenshot_path)
        print("保存成功")

        # 关闭浏览器
        print("退出中...")
        driver.quit()
        print("退出成功")
    except Exception as e:
        print(repr(e))

# 将图片分解成几个小图片
def splitStroke():
    character = '赢'
    code = ord(character)
    path = "./hanzi-data-1/out-test/%d.png" % code

    # 区域宽度和高度
    width = 128
    height = 128
    # 第一行最多显示的区域
    per_lines = 6
    # 总笔画数
    count = 17

    imgSrc = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    print(imgSrc.shape)
    for i in range(count):
        tmpImg = np.zeros((height, width, imgSrc.shape[2]), np.uint8)

        curStroke = i + 1
        # 下标值从0开始
        tmpRow = 0
        # 下标值从0开始
        tmpCol = 0
        if curStroke % per_lines == 0 :
            # 向下取整计算
            tmpRow = curStroke // per_lines - 1
            tmpCol = per_lines - 1
        else:
            # 向下取整计算
            tmpRow = curStroke // per_lines
            tmpCol = curStroke % per_lines - 1
        # 复制每一个区别的图像数据
        tmpImg[0:height, 0:width] = imgSrc[tmpRow * height : (tmpRow + 1) * height, tmpCol * width: (tmpCol + 1) * width]
        subdir = "./hanzi-data-1/out-test/%d" % code
        if not os.path.exists(subdir):
            os.mkdir(subdir)
        fileName = subdir + "/%d-%02d.png" % (code, i)
        print(fileName)
        cv2.imwrite(fileName, tmpImg)

def testFileDir():
    print(__file__)
    print(os.getcwd())

# testFileDir()
testSvg()
# testSvg2()
# splitStroke()