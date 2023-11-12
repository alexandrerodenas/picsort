import os
import shutil


def _delete_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
        print(f"Directory '{directory_path}' and its contents have been deleted.")
    except Exception as e:
        print(f"Error deleting directory '{directory_path}': {str(e)}")


def create_directory(directory_path):
    _delete_directory(directory_path)
    os.makedirs(directory_path)
    print(f"Directory '{directory_path}' created successfully.")
