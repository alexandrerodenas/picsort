from typing import List

from src.shared.config_reader import load_config
from src.shared.file_utils import create_directory, move_files
from src.shared.logger import setup_logger
from src.validation.path_validation import PathValidationsResultPrinter
from src.validation.validation_pipeline import ValidationPipeline, PathValidation


def _move_images(config, path_validations: List[PathValidation]):
    valid_directory = f"{config.output_directory}/valid"
    invalid_directory = f"{config.output_directory}/invalid"
    create_directory(valid_directory)
    create_directory(invalid_directory)
    for path_validation in path_validations:
        if path_validation.valid:
            move_files(path_validation.path, valid_directory)
        else:
            move_files(path_validation.path, invalid_directory)


def run():
    config = load_config('/../../config.yaml')
    setup_logger(config.logging_level)
    create_directory(config.output_directory)
    path_validations = ValidationPipeline(config).run_in_parallel()
    PathValidationsResultPrinter.print(path_validations)

    if config.move_files:
        _move_images(config, path_validations)


if __name__ == '__main__':
    run()
