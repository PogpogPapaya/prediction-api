import json
import requests
import nsvision as nv

label = ['ripe', 'partially', 'unripe']
image = nv.imread('./test/unknown_1.png', resize=(150, 150), normalize=True)
image = nv.expand_dims(image, axis=0)
data = json.dumps({
    "instances": image.tolist()
})

headers = {"content-type": "application/json"}

response = requests.post('http://localhost:8501/v1/models/papaya:predict', data=data, headers=headers)
print(response.json())
# result = int(response.json()['predictions'][0][0])
# print(label[result])
