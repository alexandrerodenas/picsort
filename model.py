from torchvision import models
from torchvision.models import ResNet50_Weights


def get_model_and_classes():
    with open('models/imagenet_classes.txt') as f:
        class_names = [line.strip() for line in f.readlines()]
    resnet = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
    resnet.eval()
    return resnet, class_names
