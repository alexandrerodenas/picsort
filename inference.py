import logging

import torch
from PIL import Image
from torchvision.transforms import transforms

from model import get_model_and_classes

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def _classify_image(image_path):
    image = Image.open(image_path)
    image = transform(image)
    image = image.unsqueeze(0)  # Add a batch dimension
    model, class_names = get_model_and_classes()

    with torch.no_grad():
        outputs = model(image)

    _, predicted_idx = outputs.max(1)
    predicted_class = class_names[predicted_idx]

    return predicted_class


def run_inference(images):
    logging.info(f"Inference starting")
    result = []
    for image_file in images:
        logging.debug(f"Inference on {image_file}")
        predicted_class = _classify_image(image_file)
        result.append({
            "image_file": image_file,
            "predicted_class": predicted_class
        })
    logging.info(f"Inference over")
    return result


def save_in_file(inference_result, output_file):
    with open(output_file, "w") as result_file:
        for entry in inference_result:
            result_file.write(f"image: {entry['image_file']}, class: {entry['predicted_class']}\n")

