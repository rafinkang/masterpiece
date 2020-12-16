# !pip install git+https://github.com/tensorflow/examples.git : 설치
# tensorflow를 2버전으로 upgrade
import tensorflow as tf
import pix2pix
import matplotlib.pyplot as plt

from tensorflow import keras
# from IPython.display import clear_output

class CycleganLoadWeight:
    
  __OUTPUT_CHANNELS = 3
  __BUFFER_SIZE = 1000
  __BATCH_SIZE = 1
  __IMG_WIDTH = 256
  __IMG_HEIGHT = 256
      
  # def normalize(image):
  #   image = tf.cast(image, tf.float32) # float으로 자료형 변환
  #   image = (image / 127.5) - 1
  #   return image

  def __init__(self):
    # G(X -> Y) generators생성
    self.generator_g = pix2pix.unet_generator(self.__OUTPUT_CHANNELS, norm_type='instancenorm')
    self.generator_g.load_weights("test/famous_painting/cycle_gan/vangogh.h5")
    
  # 이미지를 normalize하여 return (private function)
  def __preprocess_image_test(self, image, label):
    image = tf.cast(image, tf.float32) # float으로 자료형 변환
    image = (image / 127.5) - 1
    return image

  # 훈련된 모델에 이미지 삽입, 출력 (private function)
  def __generate_images(self, model, test_input):
    prediction = model(test_input)
      
    plt.figure(figsize=(12, 12))

    # TO-DO
    # 이미지 저장? 보여주기?
    display_list = [test_input[0], prediction[0]]
    title = ['Input Image', 'Predicted Image']

    for i in range(2):
      plt.subplot(1, 2, i+1)
      plt.title(title[i])
      # getting the pixel values between [0, 1] to plot it.
      plt.imshow(display_list[i] * 0.5 + 0.5)
      plt.axis('off')
    plt.show()

  
  def change_style(self, img_path):

    chn_style_img = tf.keras.preprocessing.image.load_img(img_path)

    chn_style_img = tf.keras.preprocessing.image.img_to_array(
        chn_style_img, data_format=None, dtype=None
    )

    chn_style_img.shape = tf.expand_dims(chn_style_img, axis=0).shape.as_list()

    chn_style_img = tf.convert_to_tensor(chn_style_img)
    chn_style_img = self.__preprocess_image_test(chn_style_img, '')
    chn_style_img = tf.image.resize(chn_style_img, [286, 286], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
    chn_style_img = tf.image.random_crop(chn_style_img, size=[1, self.__IMG_HEIGHT, self.__IMG_WIDTH, 3])

    self.__generate_images(self.generator_g, chn_style_img)

# if __name__ == "__main__":  
#     clw = CycleganLoadWeight()
#     clw.change_style('test/famous_painting/cycle_gan/test_img.jpg')
    