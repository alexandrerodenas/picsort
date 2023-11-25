from src.shared.config_reader import load_config
from src.shared.file_utils import create_directory
from src.shared.logger import setup_logger
from src.sort.sort_pipeline import SortPipeline

if __name__ == '__main__':
    config = load_config('/../../config.yaml')
    setup_logger(config.logging_level)

    create_directory(config.output_directory)

    SortPipeline(config).run_in_parallel()
