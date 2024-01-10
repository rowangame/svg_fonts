import os

import imageio

# ref1: https://blog.csdn.net/qq_14997473/article/details/90234420

'''
# 只支持png格式，需要先命名排序好(默认按照字母序排列)
# source(字符串)：素材图片路径，生成的gif也保存在该路径
# gifname(字符串)：生成的gif的文件名，命名时带后缀如：'1.gif'
# time(数字)：生成的gif每一帧的时间间隔，单位（ms）
'''
def png2gif(source, gifname, time):
    os.chdir(source) # os.chdir()：改变当前工作目录到指定的路径
    # 这里加载后,会按字母顺序排序,需要重新按数字值排序一下(否则gif图片动画显示错误)
    file_list = os.listdir() # os.listdir()：文件夹中的文件/文件夹的名字列表
    frames = [] #读入缓冲区
    for png in file_list:
        if png.endswith(".png"):
            frames.append(imageio.v2.imread(png))
    imageio.mimsave(gifname, frames, 'GIF', duration=time)

def test1():
    character = '赢'
    code = ord(character)
    source = "./hanzi-data-1/out-test/%d" % code
    gifname = "%d.gif" % code
    duration = 500
    png2gif(source, gifname, duration)

test1()