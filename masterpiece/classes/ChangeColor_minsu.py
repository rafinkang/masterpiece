
import colorsys

import cv2
import matplotlib.image as mpimg
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

# 색상 뽑기 클래스
# from Spuit import Spuit
from masterpiece.classes.Spuit import Spuit


hex = '#f3f5f2'
def hex_to_bgr(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    rgb =  list(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))
    bgr = []
    bgr.append(rgb[2])
    bgr.append(rgb[1])
    bgr.append(rgb[0])
    return bgr
# print(hex_to_bgr(hex))

def multi_hex_to_bgr(hex1,hex2,hex3,hex4):
    templist = []

    bgr1 = hex_to_bgr(hex1)
    bgr2 = hex_to_bgr(hex2)
    bgr3 = hex_to_bgr(hex3)
    bgr4 = hex_to_bgr(hex4)

    templist.append(bgr1)
    templist.append(bgr2)
    templist.append(bgr3)
    templist.append(bgr4)
    return templist
# print(multi_hex_to_bgr(hex,hex,hex,hex))

class ChangeColor_minsu:
    # def __init__(self, color_img_path, input_img_path):
    def __init__(self, hex1 ='#fcd7d6',hex2='#f4d318',hex3='#aa825a',hex4='#404223', input_img_path=None,image=None, styleType = 9):
        # self.color_img_path = color_img_path
        # self.input_img_path = input_img_path
        self.hex1 = hex1
        self.hex2 = hex2
        self.hex3 = hex3
        self.hex4 = hex4
        self.styleType = int(styleType)
        # self.change()

        if input_img_path is not None:
            self.input_img_path = input_img_path
            self.image = cv2.imread(input_img_path)
        else:
            self.image = image

    def change(self, n_cluster=4, get_plt=False):
        """
        색상을 변경해 보자.
        """
        # print("hex1 = ", self.hex1)
        # print("hex2 = ", self.hex2)
        # print("hex3 = ", self.hex3)
        # print("hex4 = ", self.hex4)
        # color_img = Spuit(self.color_img_path, n_cluster)
        input_img = Spuit(image = self.image, n_clusters=n_cluster)
        # color_img_info = color_img.get_info()
        input_img_info = input_img.get_info()
        input_img_bgr = input_img.get_image()
        input_img_labels = input_img.get_labels()

        # print('color_img_info', color_img_info)
        # print('input_img_info', input_img_info)
        # print('input_img_bgr', input_img_bgr)
        # print('input_img_labels', input_img_labels)

        if get_plt:
            # color_img.get_plt()
            input_img.get_plt()
        output_img = cv2.cvtColor(input_img_bgr, cv2.COLOR_BGR2HSV)
        # print(input_img_bgr[0][0])
        # print(output_img[0][0])

        bgr1 = hex_to_bgr(self.hex1)
        bgr2 = hex_to_bgr(self.hex2)
        bgr3 = hex_to_bgr(self.hex3)
        bgr4 = hex_to_bgr(self.hex4)
        # print(bgr1,bgr2,bgr3,bgr4)
        
        bgr1 = np.uint8([[bgr1]])
        bgr2 = np.uint8([[bgr2]])
        bgr3 = np.uint8([[bgr3]])
        bgr4 = np.uint8([[bgr4]])
        # print(bgr1)

        hsv1 = cv2.cvtColor(bgr1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(bgr2, cv2.COLOR_BGR2HSV)
        hsv3 = cv2.cvtColor(bgr3, cv2.COLOR_BGR2HSV)
        hsv4 = cv2.cvtColor(bgr4, cv2.COLOR_BGR2HSV)
        # print(hsv1)

        new_hsv = []
        new_hsv.append(hsv1[0][0])
        new_hsv.append(hsv2[0][0])
        new_hsv.append(hsv3[0][0])
        new_hsv.append(hsv4[0][0])
        # print(new_hsv[0])


        # H값 차이 계산
        convert_label2h = {}
        # for i in range(len(color_img_info)):
        #     convert_label2h[input_img_info[i]['label']] = int(input_img_info[i]['hsv'][0] - color_img_info[i]['hsv'][0])
        # for i in range(len(color_img_info)):
        for i in range(4):
            # convert_label2h[input_img_info[i]['label']] = int(
                # color_img_info[i]['hsv'][0])
            convert_label2h[input_img_info[i]['label']] = int(
                new_hsv[i][0])

        # print(convert_label2h)
        shape = output_img.shape
        # print("shape = ",shape)
        # print(convert_label2h)
        # print(shape)
        # print(type(output_img), output_img)
        # print(input_img_labels[100])
        # shape_labels = np.zeros(shape, dtype="uint8")
        # print(input_img_labels.reshape(shape[0], shape[1]))
        # print("output_img = ", output_img)
        tot = 0
        for i in range(shape[0]):
            for j in range(shape[1]):
                x = input_img_labels[tot]
                output_img[i][j][0] = int(convert_label2h[x])
                tot = tot + 1


                # s,v도 변화시켜보자
                # output_img[i][j][0] = int((new_hsv[x][0] * self.styleType + output_img[i][j][0] * (10-self.styleType) )/10)
                output_img[i][j][0] = int((new_hsv[x][0] * 9.99             + output_img[i][j][0] * (10-9.99) )/10)
                output_img[i][j][1] = int((new_hsv[x][1] * (self.styleType) + output_img[i][j][1] * (10-self.styleType))/10)
                output_img[i][j][2] = int((new_hsv[x][2] * (self.styleType) + output_img[i][j][2] * (10-self.styleType))/10)


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
        plt.axis("off")
        # plt.subplot(121)
        plt.imshow(output_img)
        # plt.subplot(122)
        # plt.imshow(blur)
        # plt.subplot(133)
        # plt.imshow(cv2.cvtColor(input_img_bgr, cv2.COLOR_BGR2RGB))
        # plt.show()

        # return output_img

        # 지연이 꺼에서 가져온 부분, 이미지를 저장하고 주소만 돌려주기
        save_img_name = 'masterpiece/static/upload_images/temp_images/' + 'color_dress_'+str(self.styleType)  + '.jpg'
        plt.savefig(save_img_name)
        # print("save_img_name :",save_img_name)
        return save_img_name


# if __name__ == "__main__":
#     colorimg = "./test/images/4color.png"
#     inputimg = "./test/images/jordy.jpg"
#     inputimg = "./test/images/su_flower.jpg"

#     hex1 = '#fcd7d6'
#     hex2 = '#f4d318'
#     hex3 = '#aa825a'
#     hex4 = '#404223'
    

#     # change_color = ChangeColor_minsu(colorimg, inputimg)
#     change_color = ChangeColor_minsu(hex1, hex2, hex3, hex4, input_img_path = inputimg)
#     # output = change_color.change(n_cluster = 4, get_plt = False)
#     output = change_color.change(n_cluster = 4, get_plt = False, styleType=9)

#     plt.imshow(output)
