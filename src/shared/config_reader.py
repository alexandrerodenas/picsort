import os

import yaml
from pydantic import BaseModel


class AppConfig(BaseModel):
    input_directory: str
    output_directory: str
    logging_level: str
    tesseract_path: str
    num_cores: int
    analysis_blurriness_threshold: int


def load_config(file_path):
    with open(os.path.dirname(__file__) + file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return AppConfig(**config_data)
