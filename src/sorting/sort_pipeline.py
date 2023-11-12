import logging

from joblib import Parallel, delayed

from src.images_loader import ImageDataLoader
from src.inference.inference import Inference
from src.pre_analysis.pre_analyzer import PreAnalyzer


class SortPipeline:
    @staticmethod
    def run_in_parallel(input_directory, tesseract_path, num_cores):
        dataframe = ImageDataLoader(input_directory).create_image_dataframe()

        logging.info("Pre analysis begins")
        pre_analyzer = PreAnalyzer(tesseract_path)
        pre_analysis = Parallel(n_jobs=num_cores)(
            delayed(
                pre_analyzer.run
            )(row) for index, row in dataframe.iterrows())
        logging.info("Pre analysis done")

        logging.info(f"Inference starting")
        inference = Inference()
        predicted_classes = Parallel(n_jobs=num_cores)(
            delayed(inference.get_top_predicted_class)(row) for index, row in
            dataframe.iterrows())
        logging.info(f"Inference over")