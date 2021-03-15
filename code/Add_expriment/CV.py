import matlab.engine


class cv:  # 加算法
    def get_cv(url, a, b):
        eng = matlab.engine.start_matlab()  # 打开matlab引擎
        result = eng.cv(url, 1, a, b)  # 返回matlab的cv函数返回的数组（坐标），cv函数（原图像地址，定位图像地址，筛选距离，迭代次数，膨胀收缩系数）
        # print(result)
        eng.quit()  # 关闭matlab引擎
        return result

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
