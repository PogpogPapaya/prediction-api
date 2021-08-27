from keras.models import load_model
import tensorflow as tf
from concurrent import futures

classList = ['medium', 'ripe', 'unripe']
my_model = load_model('./model-large.h5')

imgPath='./test.jpg'

img = tf.keras.preprocessing.image.load_img(
    imgPath, target_size=(150, 150)
)

img_array = tf.keras.preprocessing.image.img_to_array(img)
img_array = img_array / 255
img_array = img_array.reshape(1, 150, 150, 3)
predictions = my_model.predict(img_array)
print(predictions[0])

maxConfi = predictions[0][0]
index = 0


for i in range(3):
    if maxConfi < predictions[0][i]:
        maxConfi = predictions[0][i]
        index = i


print({"classification": f'{classList[index]}', "confidence": f'{maxConfi}'})