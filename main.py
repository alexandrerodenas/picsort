from analysing_image_pixels import PixelAnalysis
from images_loader import load_images
from logger import setup_logger

if __name__ == '__main__':
    setup_logger()

    image_dir = 'D:\#TODO\Portable alex - post costa rica'
    classification_result_filename = 'output/classification_results.txt'
    white_filtering_result_filename = "output/white_filtering_results.txt"
    white_filtered_images_directory = "output/whites"

    images_to_sort = load_images(image_dir)
    pixel_analysis = PixelAnalysis(images_to_sort)
    pixel_analysis.save_white_analysis_in_file(white_filtering_result_filename)

    # inference_result = run_inference(mostly_white_images)
    # inference.save_in_file(inference_result, classification_result_filename)
    # move_images(mostly_white_images, white_filtered_images_directory)
