# !pip install git+https://github.com/tensorflow/examples.git : 설치해야됨
# tensorflow를 2버전으로 upgrade해줘야함

import tensorflow as tf
from tensorflow import keras

import pix2pix

import os
import time
import matplotlib.pyplot as plt
from IPython.display import clear_output

AUTOTUNE = tf.data.experimental.AUTOTUNE

OUTPUT_CHANNELS = 3
BUFFER_SIZE = 1000
BATCH_SIZE = 1
IMG_WIDTH = 256
IMG_HEIGHT = 256

# G(X -> Y), F(Y -> X) generators생성
generator_g = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')
generator_f = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')

# D_x, D_y 생성
discriminator_x = pix2pix.discriminator(norm_type='instancenorm', target=False)
discriminator_y = pix2pix.discriminator(norm_type='instancenorm', target=False)

generator_g_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
generator_f_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

discriminator_x_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
discriminator_y_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

checkpoint_path = "test/famous_painting/gan/checkpoints"

ckpt = tf.train.Checkpoint(generator_g=generator_g,
                           generator_f=generator_f,
                           discriminator_x=discriminator_x,
                           discriminator_y=discriminator_y,
                           generator_g_optimizer=generator_g_optimizer,
                           generator_f_optimizer=generator_f_optimizer,
                           discriminator_x_optimizer=discriminator_x_optimizer,
                           discriminator_y_optimizer=discriminator_y_optimizer)

ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=5)

# if a checkpoint exists, restore the latest checkpoint.
if ckpt_manager.latest_checkpoint:
  ckpt.restore(ckpt_manager.latest_checkpoint)
  print ('Latest checkpoint restored!!')
  
# normalizing the images to [-1, 1]
def normalize(image):
  image = tf.cast(image, tf.float32) # float으로 자료형 변환
  image = (image / 127.5) - 1
  return image
  
# 수정하지 않은 이미지를 normalize하여 return
def preprocess_image_test(image, label):
  image = normalize(image)
  return image

def generate_images(model, test_input):
  prediction = model(test_input)
    
  plt.figure(figsize=(12, 12))

  display_list = [test_input[0], prediction[0]]
  title = ['Input Image', 'Predicted Image']

  for i in range(2):
    plt.subplot(1, 2, i+1)
    plt.title(title[i])
    # getting the pixel values between [0, 1] to plot it.
    plt.imshow(display_list[i] * 0.5 + 0.5)
    plt.axis('off')
  plt.show()

test_img = tf.keras.preprocessing.image.load_img('test/famous_painting/gan/test_img.jpg')

test_img = tf.keras.preprocessing.image.img_to_array(
    test_img, data_format=None, dtype=None
)

test_img.shape = tf.expand_dims(test_img, axis=0).shape.as_list()

test_img = tf.convert_to_tensor(test_img)
test_img = preprocess_image_test(test_img, '')
test_img = tf.image.resize(test_img, [286, 286], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
test_img = tf.image.random_crop(test_img, size=[1, IMG_HEIGHT, IMG_WIDTH, 3])
  
generate_images(generator_g, test_img)
