import logging
from typing import List

from joblib import Parallel, delayed

from src.images_loader import ImageDataLoader
from src.inference.inference import Inference
from src.pre_analysis.image_analysis import ImagePreAnalysis
from src.pre_analysis.pre_analyzer import PreAnalyzer
from src.shared.config_reader import AppConfig


class SortPipeline:
    @staticmethod
    def run_in_parallel(config: AppConfig):
        dataframe = ImageDataLoader(config.input_directory).create_image_dataframe()

        logging.info("Pre analysis begins")
        pre_analyzer = PreAnalyzer(config.tesseract_path)
        pre_analyzed_images: List[ImagePreAnalysis] = Parallel(n_jobs=config.num_cores)(
            delayed(
                pre_analyzer.run
            )(row) for index, row in dataframe.iterrows())
        logging.info("Pre analysis done")

        logging.info("Filtering out based on pre analysis")
        valid_pre_analyzed_images = [
            pre_analyzed_image for pre_analyzed_image in pre_analyzed_images
            if not pre_analyzed_image.is_invalid_picture(
                config.sort_conditions.blurriness_threshold,
                config.sort_conditions.white_percentage_threshold
            )
        ]
        logging.info("Filtering process done")


        logging.info(f"Inference starting")
        inference = Inference()
        predicted_classes = Parallel(n_jobs=config.num_cores)(
            delayed(inference.get_top_predicted_class)(row) for index, row in
            dataframe.iterrows())
        logging.info(f"Inference over")