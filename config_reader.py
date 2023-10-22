import yaml
from pydantic import BaseModel


class PixelAnalysisConfig(BaseModel):
    num_cores: int
    blurriness_threshold: int


class AppConfig(BaseModel):
    input_directory: str
    output_directory: str
    logging_level: str
    pixel_analysis: PixelAnalysisConfig


def load_config(file_path):
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)
    return AppConfig(**config_data)
