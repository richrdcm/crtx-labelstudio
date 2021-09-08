import logging
import numpy as np
import requests
import json
from PIL import Image
from label_studio_ml.model import LabelStudioMLBase
from label_studio_ml.utils import get_image_local_path, get_single_tag_keys, get_choice, is_skipped

logger = logging.getLogger(__name__)
feature_extractor_model = "http://localhost:8501/v1/models/resnet_deepfashion"


class CRTXnet(LabelStudioMLBase):

    def __init__(self, trainable=False, batch_size=32, epochs=3, **kwargs):
        super(CRTXnet, self).__init__(**kwargs)

        self.image_width, self.image_height = 224, 224

        self.from_name, self.to_name, self.value, self.labels_in_config = get_single_tag_keys(
            self.parsed_label_config, 'Choices', 'Image')
        self.labels = tf.convert_to_tensor(sorted(self.labels_in_config))
        num_classes = len(self.labels_in_config)


    def predict(self, tasks, **kwargs):
        image_path = get_image_local_path(tasks[0]['data'][self.value])
        image = Image.open(image_path).resize((self.image_width, self.image_height))
        image = np.array(image) / 255.0
        data = json.dumps({"signature_name": "serving_default", "instances": image.tolist()})
        headers = {"content-type": "application/json"}
        json_response = requests.post(feature_extractor_model, data=data, headers=headers)
        result = json.loads(json_response.text)['predictions']
        predictions = []
        for t in range(0, len(tasks)):
            predicted_label_idx = np.argmax(result[t], axis=-1)
            predicted_label_score = result[t][predicted_label_idx]
            predicted_label = self.labels[predicted_label_idx]
            predictions.append({
                'result': [{
                    'from_name': self.from_name,
                    'to_name': self.to_name,
                    'type': 'choices',
                    'value': {'choices': [str(predicted_label.numpy(), 'utf-8')]}
                }],
                'score': float(predicted_label_score)
            })
        return predictions

    def fit(self, completions, **kwargs):
        """This is where training happens: train your model given list of completions, then returns dict with created links and resources"""
        return {'path/to/created/model': 'label-studio/models/resnet_deepfashion/1/saved_model.pb'}
