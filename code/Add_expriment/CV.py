import os

import cv2
import matlab.engine
import numpy as np


class cv:  # 加算法
    def get_cv(url, a, b, c):
        eng = matlab.engine.start_matlab()  # 打开matlab引擎
        result = eng.cv(url, a, b, c)  # 返回matlab的cv函数返回的数组（坐标），cv函数（原图像地址，定位图像地址，筛选距离，迭代次数，膨胀收缩系数）
        # print(result)
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

    def get_march(url, min_res, dis, march_path, meth):
        ans = []
        rt = []
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
                rt.append(pt)
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
        # print("len==")
        # print(len(ans))
        ans__ = []
        img_ = cv2.imread(url)
        for i in range(len(ans)):
            ans__.append([ans[i][0] + int(w / 2), ans[i][1] + int(h / 2)])
            cv2.rectangle(img_, (int(ans[i][0]), int(ans[i][1])),
                          (int(ans[i][0] + w), int(ans[i][1]) + h), (0, 0, 137), 1)
        cv2.imwrite(r'D:\ans.png', img_)
        return ans__
