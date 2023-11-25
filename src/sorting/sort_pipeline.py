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

        predicted_classes = SortPipeline._run_inference_on_valid_images(
            config,
            valid_pre_analyzed_images
        )
        logging.info(predicted_classes)

    @staticmethod
    def _get_pre_analyzed_images(config, dataframe) -> List[ImagePreAnalysis]:
        logging.info("Pre analysis begins")
        pre_analyzer = PreAnalyzer(config.tesseract_path)
        pre_analyzed_images: List[ImagePreAnalysis] = Parallel(n_jobs=config.num_cores)(
            delayed(
                pre_analyzer.run
            )(row) for index, row in dataframe.iterrows())
        logging.info("Pre analysis done")
        return pre_analyzed_images

    @staticmethod
    def _filter_images_based_on_sort_conditions(
            config,
            pre_analyzed_images
    ) -> [List[ImagePreAnalysis], List[ImagePreAnalysis]]:
        logging.info("Filtering out based on pre analysis")
        valid_pre_analyzed_images = []
        invalid_pre_analyzed_images = []
        for pre_analyzed_image in pre_analyzed_images:
            if pre_analyzed_image.is_valid_picture(config.sort_conditions):
                valid_pre_analyzed_images.append(pre_analyzed_image)
            else:
                invalid_pre_analyzed_images.append(pre_analyzed_image)
        logging.info(f"""
            Filtering process done
            valid: {len(valid_pre_analyzed_images)}
            invalid: {len(invalid_pre_analyzed_images)}
        """)
        return valid_pre_analyzed_images, invalid_pre_analyzed_images

    @staticmethod
    def _run_inference_on_valid_images(config, valid_pre_analyzed_images) -> List[str]:
        logging.info(f"Inference starting")
        inference = Inference()
        valid_image_paths = [
            valid_pre_analyzed_image.get_path() for valid_pre_analyzed_image in valid_pre_analyzed_images
        ]
        predicted_classes = Parallel(n_jobs=config.num_cores)(
            delayed(inference.get_top_predicted_class)(valid_image_path)
            for valid_image_path in valid_image_paths
        )
        logging.info(f"Inference over")
        return predicted_classes
