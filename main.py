import analysing_image_pixels
import inference
from analysing_image_pixels import compute_white_percentage
from images_loader import load_images
from inference import run_inference
from logger import setup_logger
from move_images import move_images

if __name__ == '__main__':
    setup_logger()

    image_dir = 'input'
    classification_result_filename = 'output/classification_results.txt'
    white_filtering_result_filename = "output/white_filtering_results.txt"
    white_filtered_images_directory = "output/whites"

    images_to_sort = load_images(image_dir)
    analysed_images = compute_white_percentage(images_to_sort)
    analysing_image_pixels.save_in_file(analysed_images, white_filtering_result_filename)

    # inference_result = run_inference(mostly_white_images)
    # inference.save_in_file(inference_result, classification_result_filename)
    # move_images(mostly_white_images, white_filtered_images_directory)
