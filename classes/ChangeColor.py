
import colorsys

import cv2
import matplotlib.image as mpimg
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

# 색상 뽑기 클래스
from Spuit import *


class ChangeColor:
    def __init__(self, color_img_path, input_img_path):
        self.color_img_path = color_img_path
        self.input_img_path = input_img_path
        # self.change()

    def change(self, n_cluster=4, get_plt=False):
        """
        색상을 변경해 보자.
        """
        color_img = Spuit(self.color_img_path, n_cluster)
        input_img = Spuit(self.input_img_path, n_cluster)
        color_img_info = color_img.get_info()
        input_img_info = input_img.get_info()
        input_img_bgr = input_img.get_image()
        input_img_labels = input_img.get_labels()

        # print('color_img_info', color_img_info)
        # print('input_img_info', input_img_info)
        # print('input_img_bgr', input_img_bgr)
        # print('input_img_labels', input_img_labels)

        if get_plt:
            color_img.get_plt()
            input_img.get_plt()

        output_img = cv2.cvtColor(input_img_bgr, cv2.COLOR_BGR2HSV)

        # H값 차이 계산
        convert_label2h = {}
        # for i in range(len(color_img_info)):
        #     convert_label2h[input_img_info[i]['label']] = int(input_img_info[i]['hsv'][0] - color_img_info[i]['hsv'][0])
        for i in range(len(color_img_info)):
            convert_label2h[input_img_info[i]['label']] = int(
                color_img_info[i]['hsv'][0])

        # print(convert_label2h)
        shape = output_img.shape

        # print(convert_label2h)
        # print(shape)
        # print(type(output_img), output_img)
        # print(input_img_labels[100])
        # shape_labels = np.zeros(shape, dtype="uint8")
        # print(input_img_labels.reshape(shape[0], shape[1]))

        tot = 0
        for i in range(shape[0]):
            for j in range(shape[1]):
                x = input_img_labels[tot]
                output_img[i][j][0] = int(convert_label2h[x])
                tot = tot + 1

        # tot = 0
        # for i in range(shape[0]):
        #     for j in range(shape[1]):
        #         x = input_img_labels[tot]
        #         output_img[i][j][0] = output_img[i][j][0] + int(convert_label2h[x])
        #         tot = tot + 1

        # print(output_img)
        # print(type(output_img))

        output_img = cv2.cvtColor(output_img, cv2.COLOR_HSV2RGB)
        # blur = cv2.GaussianBlur(output_img, (5,5), 100)
        # print('mmmmmm',np.unique(cv2.cvtColor(output_img, cv2.COLOR_RGB2HSV)[:,:,0]))

        plt.figure()
        # plt.axis("off")
        plt.subplot(121)
        plt.imshow(output_img)
        plt.subplot(122)
        # plt.imshow(blur)
        # plt.subplot(133)
        plt.imshow(cv2.cvtColor(input_img_bgr, cv2.COLOR_BGR2RGB))
        plt.show()

        return output_img


if __name__ == "__main__":
    colorimg = "./test/images/4color.png"
    inputimg = "./test/images/jordy.jpg"

    change_color = ChangeColor(colorimg, inputimg)
    output = change_color.change(n_cluster = 4, get_plt = True)

    plt.imshow(output)
