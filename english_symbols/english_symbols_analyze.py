
import cv2
import numpy as np

from selenium import webdriver
from selenium.webdriver import ChromeOptions

def analyzeByChrome():
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
        driver.set_window_size(1600, 360)

        print("加载html文件")
        # 打开网页(本地文件)
        uri = "file:///E:/python/base_demo/matplotlib/svg_demo/english_symbols/res/eng-symbols-2.html"
        driver.get(uri)

        # 等待页面加载完成
        driver.implicitly_wait(5)  # 等待 5 秒钟，可以根据实际情况调整等待时间

        print("截图保存")
        # 获取页面截图
        screenshot_path = "./out/eng-symbols-2.png"
        driver.save_screenshot(screenshot_path)
        print("保存成功")

        # 关闭浏览器
        print("退出中...")
        driver.quit()
        print("退出成功")
    except Exception as e:
        print(repr(e))

# 统计一维数组的元素重复的次数
# 返回 [(开始索引,开始的值,重复的次数),,,...]
def getDeltaInfo(data: list):
    size = len(data)
    # 分析最近一行有内容的跟上一行的行数
    hInfo = []
    tmpIndex = 0
    tmpLastV = data[tmpIndex]
    tmpCount = 1
    while tmpIndex < size:
        tmpId = tmpIndex + 1
        boAssign = False
        while tmpId < size:
            if tmpLastV == data[tmpId]:
                tmpCount += 1
            else:
                hInfo.append((tmpIndex, tmpLastV, tmpCount))
                tmpIndex = tmpId
                tmpLastV = data[tmpId]
                tmpCount = 1
                boAssign = True
                break
            tmpId += 1
        # 结束后,加上没赋值的数据
        if not boAssign:
            hInfo.append((tmpIndex, tmpLastV, tmpCount))
            break
        tmpIndex = tmpIndex + 1
    return hInfo

def drawRectArea():
    img = cv2.imread("./out/eng-symbols-2.png")
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # 查找有内容标记的所有行
    height, width = imgGray.shape[:2]
    hTags = []
    for tmpH in range(height):
        boAllWhite = True
        for tmpW in range(width):
            if imgGray[tmpH, tmpW] != 255:
                boAllWhite = False
                break
        hTags.append(boAllWhite)
    print("len(hTags)", len(hTags))
    hInfo = getDeltaInfo(hTags)
    print(hInfo)
    imgBuffer = img.copy()
    # 标记内容(因模板是128x128,需要显示区域为为模板大小)
    areaInfo = []
    markColor = [0, 0, 0]
    for tmpData in hInfo:
        # 标记有内容的数据(有内容的数据记录为False)
        if tmpData[1] == False:
            tmpIndex = tmpData[0]
            tmpCount = tmpData[2]
            if tmpCount < 128:
                # 水平线
                dSpan = (128 - tmpCount) // 2
                startIdx = max(tmpIndex - dSpan, 0)
                endIdx = min(tmpIndex + tmpCount - 1 + dSpan, height-1)
                # 因dSpan整除部分会丢精度,这里需要判断是否需要加上行数据(主要保证128高度模板数据)
                deltaH = endIdx - startIdx + 1
                if 128 - deltaH > 0:
                    endIdx += 128 - deltaH
                # 标记颜色数据
                imgBuffer[startIdx, 0:width] = markColor
                imgBuffer[endIdx, 0:width] = markColor

                # 分析垂直方向的内容(按区域分析)
                vTags = []
                for tmpW in range(width):
                    boAllWhite = True
                    for tmpH in range(startIdx, endIdx + 1, 1):
                        if imgGray[tmpH,tmpW] != 255:
                            boAllWhite = False
                            break
                    vTags.append(boAllWhite)
                vInfo = getDeltaInfo(vTags)
                for tmpVTag in vInfo:
                    if tmpVTag[1] == False:
                        tmpVIdx = tmpVTag[0]
                        tmpVCnt = tmpVTag[2]
                        # startVIdx = max(tmpVIdx-1, 0)
                        # endVIdx = min(tmpVIdx + tmpVCnt - 1 + 1, width - 1)
                        startVIdx = tmpVIdx
                        endVIdx = tmpVIdx + tmpVCnt - 1
                        imgBuffer[startIdx:endIdx,startVIdx] = markColor
                        imgBuffer[startIdx:endIdx,endVIdx] = markColor
                        # 记录区域,Y开始位置,Y结束位置,X开始位置,X结束位置
                        areaInfo.append([startIdx, endIdx, startVIdx, endVIdx])
            else:
                # 上下都增加一行
                startIdx = max(tmpIndex-1,0)
                endIdx = min(tmpIndex+tmpCount-1, height-1)
                imgBuffer[startIdx, 0:width] = markColor
                imgBuffer[endIdx, 0:width] = markColor
                # 分析垂直方向的内容(按区域分析)
                vTags = []
                for tmpW in range(width):
                    boAllWhite = True
                    for tmpH in range(startIdx, endIdx + 1, 1):
                        if imgGray[tmpH, tmpW] != 255:
                            boAllWhite = False
                            break
                    vTags.append(boAllWhite)
                vInfo = getDeltaInfo(vTags)
                for tmpVTag in vInfo:
                    if tmpVTag[1] == False:
                        tmpVIdx = tmpVTag[0]
                        tmpVCnt = tmpVTag[2]
                        startVIdx = tmpVIdx
                        endVIdx = tmpVIdx + tmpVCnt - 1
                        imgBuffer[startIdx:endIdx, startVIdx] = markColor
                        imgBuffer[startIdx:endIdx, endVIdx] = markColor
                        # 记录区域,Y开始位置,Y结束位置,X开始位置,X结束位置
                        areaInfo.append([startIdx, endIdx, startVIdx, endVIdx])
    cv2.imwrite("./out/symbols-out-2.png", imgBuffer)
    trunkAreaAndSave(img, areaInfo)

def trunkAreaAndSave(img, areaInfo):
    chars = ". ? ! : ; , - ' " " { } < > ( ) [ ] ~ ` @ # $ % ^ & * | \ "
    chars = chars.replace(" ","")
    print(chars)
    for i in range(len(chars)):
        tmpArea = areaInfo[i]
        startY = tmpArea[0]
        endY = tmpArea[1]
        startX = tmpArea[2]
        endX = tmpArea[3]
        tmpH = endY - startY + 1
        tmpW = endX - startX + 1
        imgBuffer = np.zeros((tmpH, tmpW, 3), np.uint8)
        imgBuffer[0:tmpH,0:tmpW] = img[startY:endY+1,startX:endX+1]
        imgGray = cv2.cvtColor(imgBuffer, cv2.COLOR_BGR2GRAY)
        ret,imgTwo = cv2.threshold(imgGray, 254, 255, cv2.THRESH_BINARY)
        cv2.imwrite("./out/all-2/%d.png" % (ord(chars[i])), imgTwo)

# analyzeByChrome()
drawRectArea()
