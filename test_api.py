import requests
import json
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# url = "http://localhost:8080/api/projects/1/tasks/"
# url = "http://localhost:8080/api/storages/localfiles"
# url = "http://localhost:8080/api/projects/1/tasks/"
# url = "http://localhost:8080/api/current-user/whoami"
# headers = {'Authorization': 'Token crtxtoken'}
# r = requests.get(url=url, headers=headers)
# print(json.loads(r.text))

url = "http://localhost:8501/v1/models/resnet_deepfashion:predict"
dir = 'data/deepfashion/Sheer_Pleated-Front_Blouse'
img_list = []
for filename in os.listdir(dir):
       img = cv2.imread(dir + '/' + filename, cv2.IMREAD_COLOR)
       # resize 224x224
       img = cv2.resize(img, (224, 224))
       # Normalize 1./255.
       img = img * 1./255.
       img_list.append(img.tolist())

# print(img.tolist())
data = json.dumps({"signature_name": "serving_default", "instances": img_list})
headers = {"content-type": "application/json"}
json_response = requests.post(url, data=data, headers=headers)
predictions = json.loads(json_response.text)['predictions']
cat = ["Anorak", "Blazer", "Blouse", "Bomber", "Button-Down", "Cardigan", "Flannel", "Halter", "Henley", "Hoodie",
       "Jacket", "Jersey", "Parka", "Peacoat", "Poncho", "Sweater", "Tank", "Tee", "Top", "Turtleneck", "Capris", "Chinos",
       "Culottes", "Cutoffs", "Gauchos", "Jeans", "Jeggings", "Jodhpurs", "Joggers", "Leggings", "Sarong", "Shorts",
       "Skirt", "Sweatpants",  "Sweatshorts",  "Trunks",  "Caftan",  "Coat",  "Coverup",  "Dress",  "Jumpsuit",
       "Kaftan", "Kimono", "Onesie", "Robe", "Romper"]
gt = ['Blouse', ]
#print(predictions)
top = 5
idx = []
for i in range(0, len(predictions)):
       print("*"*10)
       print("GT Blouse prob: {}".format(predictions[i][2]))
       for j in range(1, top+1):
              idx = np.argmax(predictions[i])
              print("Prediction: {} top {} is {} with prob {}".format(i, j, cat[idx], predictions[i][idx]))
              predictions[i][idx] = 0.0