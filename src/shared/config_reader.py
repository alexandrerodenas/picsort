import os
from typing import List

import yaml
from pydantic import BaseModel


class ValidationConditions(BaseModel):
    text_threshold: int
    blurriness_threshold: int
    white_percentage_threshold: int
    trash_classes: List[str]


class AppConfig(BaseModel):
    input_directory: str
    image_extensions: List[str]
    move_files: bool
    output_directory: str
    logging_level: str
    tesseract_path: str
    num_cores: int
    validation_conditions: ValidationConditions
    predictions_number: int


def load_config(file_path):
    with open(os.path.dirname(__file__) + file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return AppConfig(**config_data)
