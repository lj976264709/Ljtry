import matlab.engine

class cv:#加算法
    def get_cv(url,a,b):
        eng = matlab.engine.start_matlab()  # 打开matlab引擎
        result = eng.cv(url, 1, a,b)  # 返回matlab的cv函数返回的数组（坐标），cv函数（原图像地址，定位图像地址，筛选距离，迭代次数，膨胀收缩系数）
        # print(result)
        eng.quit()  # 关闭matlab引擎
        return result
        #   [[1,3],[2,5]]