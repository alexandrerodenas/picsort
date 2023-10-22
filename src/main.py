from src.shared.config_reader import load_config
from pixel_analysis import PixelAnalysis
from images_loader import ImageDataLoader
from src.shared.file_utils import create_directory, write_dataframe_to_csv
from src.shared.logger import setup_logger

if __name__ == '__main__':
    config = load_config('/../../config.yaml')
    setup_logger(config.logging_level)

    create_directory(config.output_directory)

    dataframe = ImageDataLoader(config).get_dataframe()
    dataframe = PixelAnalysis(config).enriched(dataframe)
    write_dataframe_to_csv(dataframe, config.output_directory)

    # inference_result = run_inference(mostly_white_images)
    # inference.save_in_file(inference_result, classification_result_filename)
    # move_images(mostly_white_images, white_filtered_images_directory)
