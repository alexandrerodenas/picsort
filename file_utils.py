import os
from shutil import move
import re


def move_images(source_images, target_dir):
    for image in source_images:
        move(image, target_dir)


def create_output_directories(source_dir):
    clean_source_dir = _clean_directory_name(source_dir)
    classification_result_filename = f'output/{clean_source_dir}/classification_results.txt'
    white_filtering_result_filename = f'output/{clean_source_dir}/white_filtering_results.txt'
    white_filtered_images_directory = f'output/{clean_source_dir}/whites'
    _create_directory(f'output/{clean_source_dir}')
    _create_directory(white_filtered_images_directory)

    return classification_result_filename,white_filtering_result_filename,white_filtered_images_directory


def _clean_directory_name(directory_name):
    # Remove special characters from the directory name
    cleaned_name = re.sub(r'[^\w\s-]', '', directory_name)
    return cleaned_name


def _create_directory(directory_path):
    try:
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_path}' already exists.")
