# %%
import numpy as np
import cv2
# from google.colab.patches import cv2_imshow
import matplotlib.image as mpimg
# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import numpy as np


color_range_list = []
color_value_list = []
color_length = 0

def coloring():
    global color_length, color_range_list, color_value_list
    """
    10가지 색깔 범위 지정
    빨강 0 ~ 5, 170 ~ 180
    주황 5 ~ 25
    노랑 25 ~ 35
    연두 35 ~ 50
    초록 50 ~ 70
    하늘 70 ~ 95
    파랑 95 ~ 115
    남색 115 ~ 125
    보라 125 ~ 140
    연지 140 ~ 170
    빨강 170 ~ 180, 0 ~ 5
    """
    # hsv_cat_colorlist = []
    color_range_list = [0,5,25,35,50,70,95,115,125,140,170,180]
    
    for i in range(len(color_range_list)-1):
        color_value_list.append((color_range_list[i] + color_range_list[i+1])/2)
    # print(colorlist2)

    color_length = len(color_range_list)
    # print(color_length)

coloring()



class RainbowSpoid:
    """
    빨주노초파남보 임의로 자른 10종류의 색깔을 뽑아줌
    """
    def __init__(self, image_path):
        """
        이미지를 넣어주쎄용
        """
        self.image_path = image_path
        self.image = 0

        self.hsv_origin = []
        self.h_origin = []
        self.s_origin = []
        self.v_origin = []

        self.get_image()

        self.each_color_count_list=[]
        self.image_check()
        self.color_ranklist = []
        self.color_ranking()


    def get_image(self):
        """
        이미지 가져와서 변수에 담기
        """
        self.image = mpimg.imread(self.image_path)

        # hsv origin 담기
        self.hsv_origin = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV) # hsv 으로 바꾸기
        self.h_origin, self.s_origin, self.v_origin = cv2.split(self.hsv_origin)

        
    def plt_img(self):
        """
        이미지 띄우기
        """
        plt.imshow(self.image)
        plt.show()

    def get_hsv_origin(self):
        """
        return origin hsv array
        """
        return self.hsv_origin
    
    def get_h_origin(self):
        """
        return origin h array
        """
        return self.h_origin
    

    def image_check(self):

        # 색깔별로 같은 비중 확인 (픽셀수)  
        each_color_count_list = []
        for i in range(color_length-1):
            maskfilter = cv2.inRange(self.h_origin, color_range_list[i], color_range_list[i+1])
            each_color_count_list.append(maskfilter.sum()/255 +0.01*i)
        each_color_count_list[0] = each_color_count_list[0] + each_color_count_list[color_length-2]
        each_color_count_list.pop(color_length-2) # 마지막 중복 빨강은 삭제
        self.each_color_count_list = each_color_count_list

    def get_each_color_count_list(self):
        """
        return each_color_count_list
        """
        return self.each_color_count_list

    def color_ranking(self):
                
        sorted_color_list = self.each_color_count_list.copy()
        # print(sorted_color_list)
        sorted_color_list.sort(reverse=True)
        # print(sorted_color_list)
        
        color_ranklist = []
        for i in range(color_length-2):
            color_ranklist.append(self.each_color_count_list.index(sorted_color_list[i]))
        # print(color_ranklist) # 컬러 랭킹을 리스트에 담는다.
        self.color_ranklist = color_ranklist

    def get_color_ranking(self):
        """
        무지개 색상중 몇번째의 색상이 비중이 제일 높은지 비중별로 리스트를 만들어줌
        """
        return self.color_ranklist


class ColorTrade:
    """
    이미지 2개 받아서 색 치환해줌
    """
    def __init__(self, image_path1, image_path2):
        """
        이미지 2개를 넣어주쎄용
        """
        self.image_path1 = image_path1
        self.image_path2 = image_path2
        self.new_h = []
        self.traded_hsv = []
        self.remaked_image = []
        
        RS1 = RainbowSpoid(self.image_path1)
        RS2 = RainbowSpoid(self.image_path2)

        self.hsv_origin1 = RS1.get_hsv_origin()
        self.h_origin1 = RS1.get_h_origin()
        self.color_ranklist1 = RS1.get_color_ranking()
        self.color_ranklist2 = RS2.get_color_ranking()
        self.make_new_h()
        self.color_trade_h()



    def get_hsv_origin1(self):
        return self.hsv_origin1
        
    def get_h_origin1(self):
        return self.h_origin1

    def make_new_h(self):
        self.new_h = self.h_origin1[:,:].copy()
        self.new_h[:,:] = 0

    def color_trade_h(self):
                
        for i in range(color_length-2):
        # i = 0
            maskfilter = cv2.inRange(self.h_origin1, color_range_list[self.color_ranklist1[i]], color_range_list[self.color_ranklist1[i]+1]) # 색깔 레인지 정해서 그부분만 255로 바꾸기
            maskfilter = maskfilter/255*color_value_list[self.color_ranklist2[i]]
            self.new_h = self.new_h + maskfilter

        self.traded_hsv = self.hsv_origin1.copy()
        self.traded_hsv[:,:,0] = self.new_h
        
        # self.remaked_image = cv2.cvtColor(self.traded_hsv, cv2.COLOR_HSV2BGR) # hsv를 rgb로 바꾸기
        self.remaked_image = cv2.cvtColor(self.traded_hsv, cv2.COLOR_HSV2RGB) 
        # print(self.remaked_image)
        # self.remaked_image[:,:,0],self.remaked_image[:,:,1],self.remaked_image[:,:,2] = self.remaked_image[:,:,1],self.remaked_image[:,:,2],self.remaked_image[:,:,0]
        # self.remaked_image = self.remaked_image *255
        # self.remaked_image = list(map(int, self.remaked_image))

        self.remaked_image = np.array(self.remaked_image,dtype=int)
        # self.remaked_image = self.remaked_image.tolist()
        # print(self.remaked_image)
        # print(self.remaked_image.shape)
        # print(type(self.remaked_image))
        



    def get_traded_hsv(self):
        return self.traded_hsv
    
    def plt_img(self):
        """
        이미지 띄우기
        """
        # print(self.remaked_image)
        # plt.figure()
        plt.imshow(self.remaked_image)
        plt.show()
        # cv2.imshow('self.remaked_image',self.remaked_image)


# image_path1 = "./test/images/butterfly.jpeg"
# image_path2 = "./test/images/red.jpeg"

# CT = ColorTrade(image_path1,image_path2)
# CT.plt_img()

