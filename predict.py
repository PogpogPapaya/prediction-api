from keras.models import load_model
my_model = load_model('./model-large.h5')
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
classList = ['medium','ripe','unripe']
base_test = './test/'
pictures = list(map(lambda x:base_test+x,os.listdir(base_test)))
print(pictures)
for i in pictures:
  img = tf.keras.preprocessing.image.load_img(
      i, target_size=(150, 150)
  )
  img_array = tf.keras.preprocessing.image.img_to_array(img)
  img_array = img_array / 255
  img_array = img_array.reshape(1,150,150,3)
  predictions = my_model.predict(img_array)
  print(predictions)
#   imgplot = plt.imshow(img)
#   plt.show()
#   print(classList[np.argmax(predictions[0])])