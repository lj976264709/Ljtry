import os

import cv2
import matlab.engine
import numpy as np
from PIL import Image
from numpy import array


class cv:  # 加算法
    def get_cv(url, a, b, c):
        eng = matlab.engine.start_matlab()  # 打开matlab引擎
        result = eng.cv(url, a, b, c)  # 返回matlab的cv函数返回的坐标数组，cv函数（原图像地址，筛选距离，迭代次数，膨胀收缩系数）
        eng.quit()  # 关闭matlab引擎
        return result

    def get_CLI(url, ot_url):
        print(url)
        eng = matlab.engine.start_matlab()  # 打开matlab引擎
        eng.VegetationIndex(url, ot_url)
        eng.quit()  # 关闭matlab引擎

    def get_fenshuiling(url, a):
        a = float(a)
        print("ok")
        eng = matlab.engine.start_matlab()
        result = eng.marked_watershed(url, a)
        eng.quit()
        return result

    def get_fenshuiling_g(url, a, b):
        a = float(a)
        print("ok")
        eng = matlab.engine.start_matlab()
        result = eng.gradient_watershed(url, a, b)
        eng.quit()
        return result

    def get_maximum(url, mol, min):
        img = array(Image.open(url).convert('L'), 'f')
        # height = img.shape[0]  # 将tuple中的元素取出，赋值给height，width，channels
        # width = img.shape[1]
        # print(height, width)
        # im = mw.ImageOriginal
        im = cv2.imread(url)
        # im = Image.open("lena2.jpg")
        # mol = 47
        maximun = []
        changyu = img.shape[1] % mol  # 图片长度和模板的余数
        changbei = img.shape[1] // mol  # 图片长除以模板大小，取整
        kuanyu = img.shape[0] % mol  # 图片宽度和模板的余数
        kuanbei = img.shape[0] // mol  # 图片宽除以模板大小，取整
        for row in range(0, img.shape[0] - mol, mol):  # 遍历每一行
            for col in range(0, img.shape[1] - mol, mol):
                # gray_min = 255
                gray_min = 0
                gray_max = 0
                max_x = -1
                max_y = -1
                # 此步骤筛选出全局最小值
                for i in range(0, mol):  # 遍历窗口内每一行
                    for j in range(0, mol):  # 遍历窗口内每一行
                        if img[row + i, col + j] >= gray_min:
                            gray_min = img[row + i, col + j]
                            max_x = row + i  # 窗口内灰度值最小的点横坐标
                            max_y = col + j  # 窗口内灰度值最小的点纵坐标
                # print(gray_min, max_x, max_y)
                # cv2.circle(im, (max_y, max_x), 1, (30, 255, 255), 2)
                # maximun.append([max_y, max_x])
                if gray_min > min:
                    # print(gray_min, max_x, max_y)
                    # cv2.circle(im, (max_y, max_x), 1, (30, 255, 255), 2)
                    maximun.append([max_y, max_x])

        if changyu > 0:

            col = mol * changbei  # 遍历每一行
            for row in range(0, img.shape[0] - mol, mol):  # 遍历每一列

                gray_min = 0
                max_x = -1
                max_y = -1
                for j in range(0, changyu):  # 遍历窗口内每一行
                    for i in range(0, mol):  # 遍历窗口内每一行
                        if img[row + i, col + j] >= gray_min:
                            gray_min = img[row + i, col + j]
                            max_x = row + i  # 窗口内灰度值最小的点横坐标
                            max_y = col + j  # 窗口内灰度值最小的点纵坐标
                # print(gray_min, max_x, max_y)
                # cv2.circle(img, (max_x, max_y), 1, (0, 0, 0), 2)#黄色
                # cv2.circle(im, (max_y, max_x), 1, (30, 255, 255), 2)
                # maximun.append([max_y, max_x])
                if gray_min > min:
                    # print(gray_min, max_x, max_y)
                    # cv2.circle(im, (max_y, max_x), 1, (30, 255, 255), 2)
                    maximun.append([max_y, max_x])
        if kuanyu > 0:

            row = mol * kuanbei  # 遍历每一行
            for col in range(0, img.shape[1] - mol, mol):  # 遍历每一列

                gray_min = 0
                max_x = -1
                max_y = -1
                for j in range(0, mol):  # 遍历窗口内每一行
                    for i in range(0, kuanyu):  # 遍历窗口内每一行
                        if img[row + i, col + j] >= gray_min:
                            gray_min = img[row + i, col + j]
                            max_x = row + i  # 窗口内灰度值最小的点横坐标
                            max_y = col + j  # 窗口内灰度值最小的点纵坐标
                # print(gray_min, max_x, max_y)
                # cv2.circle(img, (max_x, max_y), 1, (0, 0, 0), 2)  # 黄色
                # cv2.circle(im, (max_y, max_x), 1, (30, 255, 255), 2)
                # maximun.append([max_y, max_x])
                if gray_min > min:
                    # print(gray_min, max_x, max_y)
                    # cv2.circle(im, (max_y, max_x), 1, (30, 255, 255), 2)
                    maximun.append([max_y, max_x])
        if changyu > 0 and kuanyu > 0:

            col = mol * changbei  # 遍历每一行
            row = mol * kuanbei  # 遍历每一列

            gray_min = 0
            max_x = -1
            max_y = -1
            for j in range(0, changyu):  # 遍历窗口内每一行
                for i in range(0, kuanyu):  # 遍历窗口内每一行
                    if img[row + i, col + j] >= gray_min:
                        gray_min = img[row + i, col + j]
                        max_x = row + i  # 窗口内灰度值最小的点横坐标
                        max_y = col + j  # 窗口内灰度值最小的点纵坐标
            # print(gray_min, max_x, max_y)
            # cv2.circle(img, (max_x, max_y), 1, (0, 0, 0), 2)  # 黄色
            # cv2.circle(im, (max_y, max_x), 1, (30, 255, 255), 2)
            # maximun.append([max_y, max_x])
            if gray_min > min:
                # print(gray_min, max_x, max_y)
                # cv2.circle(im, (max_y, max_x), 1, (30, 255, 255), 2)
                maximun.append([max_y, max_x])
        return maximun

    def get_march(url, min_res, dis, march_path, meth):
        ans = []
        rt = []
        img_ = cv2.imread(url)
        print(url, min_res, march_path, meth)
        img = cv2.imread(url, 0)
        for tp in os.walk(march_path):
            list_mb = tp[2]
            break
        for tp in list_mb:
            rt.clear()
            mb_path = march_path + '\\' + tp
            template = cv2.imread(mb_path, 0)
            w, h = template.shape[::-1]
            method = eval(meth)
            res = cv2.matchTemplate(img, template, method)
            loc = np.where(res > min_res)
            for pt in zip(*loc[::-1]):
                rt.append([pt[0] + int(w / 2), pt[1] + int(h / 2)])

            vis = [0] * len(rt)
            for i in range(len(rt)):
                if vis[i] == 1:
                    continue
                for j in range(i + 1, len(rt)):
                    if vis[j] == 1:
                        continue
                    if (rt[i][0] - rt[j][0]) ** 2 + (rt[i][1] - rt[j][1]) ** 2 < dis:
                        vis[j] = 1
            if len(ans) == 0:
                for i in range(len(rt)):
                    if vis[i] == 0:
                        ans.append(rt[i])
            else:
                sz = len(ans)
                for j in range(len(rt)):
                    if vis[j] == 1:
                        continue
                    flag = True
                    for i in range(sz):
                        if (ans[i][0] - rt[j][0]) ** 2 + (ans[i][1] - rt[j][1]) ** 2 < dis:
                            flag = False
                            break
                    if flag:
                        ans.append(rt[j])
            for i in range(len(ans)):
                cv2.rectangle(img_, (int(ans[i][0] - w / 2), int(ans[i][1] - h / 2)),
                              (int(ans[i][0] + w / 2), int(ans[i][1] + h / 2)), (0, 0, 137), 1)
        # print("len==")
        # print(len(ans))
        ans__ = []
        for i in range(len(ans)):
            ans__.append(ans[i])
            # cv2.rectangle(img_, (int(ans[i][0]), int(ans[i][1])),
            #               (int(ans[i][0] + w), int(ans[i][1]) + h), (0, 0, 137), 1)
        cv2.imwrite(r'D:\ans.png', img_)
        return ans__
