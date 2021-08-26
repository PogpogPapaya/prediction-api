from fastapi import FastAPI, File, UploadFile
import uuid
import os
from keras.models import load_model
import tensorflow as tf
import sys

app = FastAPI()

@app.get("/api/ping")
async def root():
    return {"message": "pong"}

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    imgId = uuid.uuid4()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    imgPath = f'{dir_path}/{imgId}'
    f = open(f'{imgPath}', 'wb')
    content = await file.read()
    f.write(content)

    my_model = load_model('./model-large.h5')

    classList = ['medium', 'ripe', 'unripe']

    img = tf.keras.preprocessing.image.load_img(
        imgPath, target_size=(150, 150)
    )

    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array / 255
    img_array = img_array.reshape(1, 150, 150, 3)
    predictions = my_model.predict(img_array)

    maxConfi = predictions[0][0]
    index = 0

    os.remove(imgPath)

    for i in range(3):
        if maxConfi < predictions[0][i]:
            maxConfi = predictions[0][i]
            index = i


    return {"classification": f'{classList[index]}', "confidence": f'{maxConfi}'}