import torch
from PIL import Image
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights


class PredictionsForPath:
    def __init__(self, path, predicted_classes):
        self.path = path
        self.predicted_classes = predicted_classes

    def has_trash_class(self, trash_classes) -> bool:
        return bool(set(self.predicted_classes) & set(trash_classes))


class Inference:
    def __init__(self, predictions_number):
        self.model, self.classes = self._get_model_and_classes()
        self.predictions_number = predictions_number

    def get_predictions_for_path(self, path: str) -> PredictionsForPath:
        img_tensor = self._to_image_tensor(path)

        with torch.no_grad():
            output = self.model(img_tensor)

        _, predicted_idx = torch.topk(output, self.predictions_number)
        top_classes = [self.classes[idx.item()] for idx in predicted_idx[0]]

        return PredictionsForPath(
            path,
            top_classes
        )

    @staticmethod
    def _get_model_and_classes():
        with open('./../models/imagenet_classes.txt') as f:
            class_names = [line.strip() for line in f.readlines()]
        resnet = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
        resnet.eval()
        return resnet, class_names

    @staticmethod
    def _to_image_tensor(img_path):
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        img = Image.open(img_path)
        img_tensor = preprocess(img)
        img_tensor = torch.unsqueeze(img_tensor, 0)  # Add batch dimension
        return img_tensor
