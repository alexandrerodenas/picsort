import os
import shutil


def write_dataframe_to_csv(df, output_dir):
    file_path = output_dir + "/dataframe.csv"
    try:
        df.drop(columns=['content'], inplace=True)
        df.to_csv(file_path, index=False)
        print(f"DataFrame successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing DataFrame to {file_path}: {str(e)}")


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
