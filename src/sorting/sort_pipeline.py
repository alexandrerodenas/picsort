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

        pre_analyzed_images = SortPipeline._get_pre_analyzed_images(config, dataframe)

        valid_pre_analyzed_images, invalid_pre_analyzed_images = SortPipeline._filter_images_based_on_sort_conditions(
            config,
            pre_analyzed_images
        )

        logging.info(f"Inference starting")
        inference = Inference()
        predicted_classes = Parallel(n_jobs=config.num_cores)(
            delayed(inference.get_top_predicted_class)(row) for index, row in
            dataframe.iterrows())
        logging.info(f"Inference over")

    @staticmethod
    def _filter_images_based_on_sort_conditions(config, pre_analyzed_images):
        logging.info("Filtering out based on pre analysis")
        valid_pre_analyzed_images = []
        invalid_pre_analyzed_images = []
        for pre_analyzed_image in pre_analyzed_images:
            if pre_analyzed_image.is_valid_picture(config.sort_conditions):
                valid_pre_analyzed_images.append(pre_analyzed_image)
            else:
                invalid_pre_analyzed_images.append(pre_analyzed_image)
        logging.info("Filtering process done")
        return valid_pre_analyzed_images, invalid_pre_analyzed_images

    @staticmethod
    def _get_pre_analyzed_images(config, dataframe):
        logging.info("Pre analysis begins")
        pre_analyzer = PreAnalyzer(config.tesseract_path)
        pre_analyzed_images: List[ImagePreAnalysis] = Parallel(n_jobs=config.num_cores)(
            delayed(
                pre_analyzer.run
            )(row) for index, row in dataframe.iterrows())
        logging.info("Pre analysis done")
        return pre_analyzed_images
