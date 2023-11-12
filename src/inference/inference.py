import logging
import torch
import pandas as pd
from joblib import Parallel, delayed

from src.inference.model import get_model_and_classes, to_image_tensor
from src.shared.dataframe_utils import vertical_concat


class Inference:
    def __init__(self, num_cores):
        self.num_cores = num_cores
        self.model, self.classes = get_model_and_classes()

    def add_predicted_classes(self, images_dataframe):
        logging.info(f"Inference starting")
        results = Parallel(n_jobs=self.num_cores)(
            delayed(self._load_and_preprocess_image_and_get_predicted_class)(row) for index, row in images_dataframe.iterrows())
        predicted_class_as_dataframe = pd.DataFrame(results, columns=['predicted_classes'])
        logging.info(f"Inference over")
        return vertical_concat(images_dataframe, predicted_class_as_dataframe)

    def _load_and_preprocess_image_and_get_predicted_class(self, row):
        image_path = row['path']
        img_tensor = to_image_tensor(image_path)

        with torch.no_grad():
            output = self.model(img_tensor)

        _, predicted_idx = torch.max(output, 1)
        return self.classes[predicted_idx.item()]