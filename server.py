
import uuid
import os
import grpc
from keras.models import load_model
import tensorflow as tf
from concurrent import futures
import prediction_service_pb2
import prediction_service_pb2_grpc

my_model = load_model('./model-large.h5')

class PapayaServiceServicer(prediction_service_pb2_grpc.PapayaServiceServicer):
    def Predict(self, request, context):
        imgId = uuid.uuid4()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        imgPath = f'{dir_path}/{imgId}'
        # write request.imege to file
        with open(imgPath, 'wb') as binary_file:
            binary_file.write(request.image)
        
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

        return prediction_service_pb2.PredictionResponse(
            label=f'{classList[index]}', confidence=maxConfi
        )

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  prediction_service_pb2_grpc.add_PapayaServiceServicer_to_server(
      PapayaServiceServicer(), server)
  server.add_insecure_port('[::]:8000')
  print("Starting on port 8000...")
  server.start()
  server.wait_for_termination()

serve()