import logging

import cv2
from joblib import Parallel, delayed

from src.inference.inference import Inference
from src.load.images_loader import ImagesLoader
from src.pre_analysis.pre_analyzer import PreAnalyzer
from src.shared.config_reader import AppConfig
from src.validation.path_validation import PathValidation, InvalidPath, ValidPath


class ValidationPipeline:
    def __init__(self, config: AppConfig):
        self.input_directory = config.input_directory
        self.image_extensions = config.image_extensions
        self.tesseract_path = config.tesseract_path
        self.num_cores = config.num_cores
        self.sort_conditions = config.validation_conditions
        self.predictions_number = config.number_of_class_to_predict

    def run_in_parallel(self):
        image_paths = ImagesLoader(
            self.input_directory,
            self.image_extensions
        ).extract_paths()

        inference = Inference(self.predictions_number)

        logging.info("Running validation on images")
        path_validations = Parallel(n_jobs=self.num_cores)(
            delayed(self._filter_image)(image_path, inference)
            for image_path in image_paths
        )
        return path_validations

    def _filter_image(self, image_path, inference) -> PathValidation:
        image_content = cv2.imread(image_path)
        image_grayscale = cv2.cvtColor(image_content, cv2.COLOR_BGR2GRAY)

        white_percentage = PreAnalyzer.get_white_percentage(image_grayscale)
        if white_percentage > self.sort_conditions.white_percentage_threshold:
            return InvalidPath(image_path, "white", f"White percentage: {white_percentage}")

        blurriness_level = PreAnalyzer.get_blur_level(image_grayscale)
        if blurriness_level > self.sort_conditions.blurriness_threshold:
            return InvalidPath(image_path, "blurriness", f"Blurriness level: {blurriness_level}")

        text = PreAnalyzer.get_text(image_content, self.tesseract_path)
        text_length = len(text)
        if text_length > self.sort_conditions.text_threshold:
            return InvalidPath(image_path, "text", f"Text length: {text_length} ({text})")

        else:
            predictions_for_path = inference.get_predictions_for_path(image_path)
            if predictions_for_path.has_trash_class(self.sort_conditions.trash_classes):
                return InvalidPath(image_path, "nature", f"Trash class detected: {predictions_for_path.predicted_classes}")
            else:
                return ValidPath(image_path)
