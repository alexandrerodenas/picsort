from pixel_analysis import PixelAnalysis
from file_utils import create_output_directories
from images_loader import ImageDataLoader
from logger import setup_logger

if __name__ == '__main__':
    setup_logger()

    image_dir = "input"
    (classification_result_filename,
     white_filtering_result_filename,
     white_filtered_images_directory) = create_output_directories(image_dir)

    dataframe = ImageDataLoader(image_dir).get_dataframe()
    dataframe = PixelAnalysis().enriched_with_white_analysis(dataframe)

    # inference_result = run_inference(mostly_white_images)
    # inference.save_in_file(inference_result, classification_result_filename)
    # move_images(mostly_white_images, white_filtered_images_directory)
