import cv2

import time


class Image_mark:
    def mark_function(list, url,sz):  # 目视标记
        images = cv2.imread(url)  # 打开原图
        for i in range(len(list)):
            cv2.circle(images, (int(list[i][0]), int(list[i][1])), int(sz), (255, 0, 0), -1)
        cv2.imwrite('D:/23.jpg', images)  # 写入标记后的图

    def mark_function_2(right_list, wrong_list, last_list, url, js_url,sz):  # 对比结果标记
        sz=int(sz)
        images_js = cv2.imread(url)
        for i in range(len(right_list)):
            cv2.circle(images_js, (int(right_list[i][0]), int(right_list[i][1])), sz, (255, 0, 0), -1)
        for i in range(len(wrong_list)):
            cv2.circle(images_js, (int(wrong_list[i][0]), int(wrong_list[i][1])), sz, (255, 0, 0), -1)
        cv2.imwrite(js_url, images_js)

        images = cv2.imread(url)  # 打开原图
        for i in range(len(right_list)):
            cv2.circle(images, (int(right_list[i][0]), int(right_list[i][1])),sz , (0, 255, 255), -1)
        for i in range(len(wrong_list)):
            cv2.line(images, (int(wrong_list[i][0]) - sz, int(wrong_list[i][1]) - sz),
                     (int(wrong_list[i][0]) + sz, int(wrong_list[i][1]) + sz), ( 0, 0,139), int(sz/2))
            cv2.line(images, (int(wrong_list[i][0]) - sz, int(wrong_list[i][1]) + sz),
                     (int(wrong_list[i][0]) + sz, int(wrong_list[i][1]) - sz), ( 0, 0,139), int(sz/2))
        for i in range(len(last_list)):
            cv2.rectangle(images, (int(last_list[i][0]) - sz, int(last_list[i][1] - sz)),
                          (int(last_list[i][0]) + sz, int(last_list[i][1]) + sz), (255, 255, 0), -1)
        cv2.imwrite('D:/66.jpg', images)  # 写入标记后的图
