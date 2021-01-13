import cv2

import time


class Image_mark:
    def mark_function(list, url):  # 目视标记
        images = cv2.imread(url)  # 打开原图
        for i in range(len(list)):
            cv2.circle(images, (int(list[i][0]), int(list[i][1])), 1, (255, 0, 0), 4)
        cv2.imwrite('D:/23.jpg', images)  # 写入标记后的图

    def mark_function_2(right_list, wrong_list, last_list, url, js_url):  # 对比结果标记
        images_js = cv2.imread(url)
        for i in range(len(right_list)):
            cv2.circle(images_js, (int(right_list[i][0]), int(right_list[i][1])), 1, (255, 0, 0), 2)
        for i in range(len(wrong_list)):
            cv2.circle(images_js, (int(wrong_list[i][0]), int(wrong_list[i][1])), 1, (255, 0, 0), 2)
        cv2.imwrite(js_url, images_js)

        images = cv2.imread(url)  # 打开原图
        for i in range(len(right_list)):
            cv2.circle(images, (int(right_list[i][0]), int(right_list[i][1])), 1, (0, 255, 255), 2)
        for i in range(len(wrong_list)):
            cv2.line(images, (int(wrong_list[i][0]) - 2, int(wrong_list[i][1]) - 2),
                     (int(wrong_list[i][0]) + 2, int(wrong_list[i][1]) + 2), ( 0, 0,139), 1)
            cv2.line(images, (int(wrong_list[i][0]) - 2, int(wrong_list[i][1]) + 2),
                     (int(wrong_list[i][0]) + 2, int(wrong_list[i][1]) - 2), ( 0, 0,139), 1)
        for i in range(len(last_list)):
            cv2.rectangle(images, (int(last_list[i][0]) - 2, int(last_list[i][1] - 2)),
                          (int(last_list[i][0]) + 2, int(last_list[i][1]) + 2), (255, 255, 0), -1)
        cv2.imwrite('D:/66.jpg', images)  # 写入标记后的图
