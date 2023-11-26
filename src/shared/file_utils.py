import logging
import os
import shutil


def _delete_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
        logging.info(f"Directory '{directory_path}' and its contents have been deleted.")
    except Exception as e:
        logging.warning(f"Error deleting directory '{directory_path}': {str(e)}")


def create_directory(directory_path):
    if os.path.exists(directory_path):
        logging.warning(f"Directory '{directory_path}' already exists. Skipping creation.")
    else:
        os.makedirs(directory_path)
        logging.info(f"Directory '{directory_path}' created successfully.")


def move_files(file_path, destination_directory):
    if not os.path.exists(destination_directory):
        logging.error(f"Destination directory '{destination_directory}' does not exist.")
        return

    if not os.path.exists(file_path):
        logging.warning(f"File '{file_path}' does not exist. Skipping.")
        return

    file_name = os.path.basename(file_path)
    destination_path = os.path.join(destination_directory, file_name)

    try:
        shutil.move(file_path, destination_path)
        logging.debug(f"Moved '{file_name}' to {destination_directory}")
    except Exception as e:
        logging.error(f"Error moving '{file_name}': {e}")
