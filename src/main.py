from src.shared.config_reader import load_config
from src.shared.file_utils import create_directory, move_files
from src.shared.logger import setup_logger
from src.sort.sort_pipeline import SortPipeline


def move_images():
    valid_directory = f"{config.output_directory}/valid"
    invalid_directory = f"{config.output_directory}/invalid"
    create_directory(valid_directory)
    create_directory(invalid_directory)
    move_files(valid_images_paths, valid_directory)
    move_files(invalid_images_paths, invalid_directory)


if __name__ == '__main__':
    config = load_config('/../../config.yaml')
    setup_logger(config.logging_level)

    create_directory(config.output_directory)

    valid_images_paths, invalid_images_paths = SortPipeline(config).run_in_parallel()

    #move_images()

