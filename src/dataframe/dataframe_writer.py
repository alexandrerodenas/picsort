import logging


class DataFrameWriter:
    def __init__(self, dataframe, excluded_columns=None):
        if excluded_columns is None:
            excluded_columns = []
        self.dataframe = dataframe.drop(columns=excluded_columns, errors='ignore')

    def write_dataframe_to_csv(self, output_dir):
        file_path = output_dir + "/dataframe.csv"
        try:
            self.dataframe.to_csv(file_path, index=False)
            logging.info(f"DataFrame successfully written to {file_path}")
        except Exception as e:
            logging.error(f"Error writing DataFrame to {file_path}: {str(e)}")

