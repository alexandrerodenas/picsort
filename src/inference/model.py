import torch
from PIL import Image
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights


def get_model_and_classes():
    with open('./../models/imagenet_classes.txt') as f:
        class_names = [line.strip() for line in f.readlines()]
    resnet = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    resnet.eval()
    return resnet, class_names


def to_image_tensor(img_path):
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
