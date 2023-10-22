from pixel_analysis import PixelAnalysis
from file_utils import create_directory, write_dataframe_to_csv
from images_loader import ImageDataLoader
from logger import setup_logger

if __name__ == '__main__':
    setup_logger()

    image_dir = "input"
    output_dir = "output"
    create_directory(output_dir)

    dataframe = ImageDataLoader(image_dir).get_dataframe()
    dataframe = PixelAnalysis().enriched_with_white_analysis(dataframe)
    write_dataframe_to_csv(dataframe, output_dir)


    # inference_result = run_inference(mostly_white_images)
    # inference.save_in_file(inference_result, classification_result_filename)
    # move_images(mostly_white_images, white_filtered_images_directory)
