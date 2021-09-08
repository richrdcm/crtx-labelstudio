"""
This script use label-studio API to setup the deepfashion dataset and the SOEX test-dataset
"""

import requests
import json
import time
import os

#host = 'http://' + os.environ["LS_HOST"] + ':' + str(os.environ["LS_PORT"] + '/')
host = 'http://crtx-label-studio:8080/'
user = {'username': os.environ["LS_USERNAME"], 'password': os.environ["LS_PASSWORD"]}
headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + os.environ['LS_TOKEN']}

# Create project
conf_file = "/label-studio/conf/deepfashion_categories.xml"
with open(conf_file) as xml:
  label_config = xml.read()
url = host + 'api/projects'
project = {
  "title": "crtx",
  "description": "Data visualization and labeling fro the CRTX project",
  "label_config": label_config,
  "expert_instruction": "Follow CRTX labeling-strategy",
  "show_instruction": 'true',
  "show_skip_button": 'true',
  "enable_empty_annotation": 'true',
  "show_annotation_history": 'true',
  "task_data_login": "admin@crtx.com",
  "task_data_password": "12345678",
  "control_weights": {},
  "evaluate_predictions_automatically": 'true'
}
r = requests.post(url=url, data=json.dumps(project), headers=headers)
print(json.loads(r.text))

# Add the local storage
current_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
create_storage = {
  "path": "/label-studio/data/deepfashion",
  "regex_filter": "",
  "use_blob_urls": 'true',
  "title": "deepfashion",
  "description": "Categories and attributes from deepfashion database",
  "last_sync": current_time,
  "last_sync_count": '0',
  "project": '1'
}
url = host + 'api/storages/localfiles'
r = requests.post(url=url, data=json.dumps(create_storage), headers=headers)
print(json.loads(r.text))

# Sync the local storage once
url = host + "api/storages/localfiles/1/sync"
sync_local = {
  "path": "/label-studio/data/deepfashion",
  "regex_filter": "",
  "use_blob_urls": 'true',
  "title": "deepfashion",
  "description": "Categories and attributes from deepfashion database",
  "last_sync": current_time,
  "last_sync_count": '0',
  "project": '1'
}
# r = requests.post(url=url, data=json.dumps(sync_local), headers=headers)
# print(json.loads(r.text))

# Load Annotations
ann_file = open("/label-studio/src/data/deepfashion_prelabels.json")
ann_json = json.load(ann_file)

headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + os.environ['LS_TOKEN']}
url = host + "api/projects/1/import"
r = requests.post(url=url, data=json.dumps(ann_json), headers=headers)
print(json.loads(r.text))

