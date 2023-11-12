import logging
import torch
import pandas as pd
from joblib import Parallel, delayed

from src.inference.model import get_model_and_classes, to_image_tensor
from src.shared.dataframe_utils import vertical_concat


class Inference:
    def __init__(self):
        self.model, self.classes = get_model_and_classes()

    def get_top_predicted_class(self, row):
        img_tensor = to_image_tensor(row["path"])

        with torch.no_grad():
            output = self.model(img_tensor)

        _, predicted_idx = torch.max(output, 1)
        return self.classes[predicted_idx.item()]