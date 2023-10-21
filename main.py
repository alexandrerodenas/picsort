import logging

from filtering_image import filtering_mostly_white_images
from images_loader import load_images
from inference import run_inference
from logger import setup_logger

if __name__ == '__main__':
    setup_logger()

    image_dir = 'sauvegarde_alex'
    output_file = 'classification_results.txt'

    images_to_sort = load_images(image_dir)
    mostly_white_images = filtering_mostly_white_images(images_to_sort)
    inference_result = run_inference(mostly_white_images)
