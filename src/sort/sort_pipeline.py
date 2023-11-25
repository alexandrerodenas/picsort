import logging
from typing import List

from joblib import Parallel, delayed

from src.inference.inference import Inference
from src.load.images_loader import ImageDataLoader
from src.pre_analysis.image_analysis import ImagePreAnalysis
from src.pre_analysis.pre_analyzer import PreAnalyzer


class SortPipeline:

    def __init__(self, config):
        self.input_directory = config.input_directory
        self.image_extensions = config.image_extensions
        self.tesseract_path = config.tesseract_path
        self.num_cores = config.num_cores
        self.sort_conditions = config.sort_conditions

    def run_in_parallel(self):
        dataframe = ImageDataLoader(
            self.input_directory,
            self.image_extensions
        ).create_image_dataframe()

        pre_analyzed_images = self._get_pre_analyzed_images(dataframe)

        valid_pre_analyzed_images, invalid_pre_analyzed_images = self._filter_images_based_on_sort_conditions(
            pre_analyzed_images
        )

        predicted_classes = self._run_inference_on_valid_images(
            valid_pre_analyzed_images
        )

    def _get_pre_analyzed_images(self, dataframe) -> List[ImagePreAnalysis]:
        logging.info("Pre analysis begins")
        pre_analyzer = PreAnalyzer(self.tesseract_path)
        pre_analyzed_images: List[ImagePreAnalysis] = Parallel(n_jobs=self.num_cores)(
            delayed(
                pre_analyzer.run
            )(row) for index, row in dataframe.iterrows())
        logging.info("Pre analysis done")
        return pre_analyzed_images

    def _filter_images_based_on_sort_conditions(
            self,
            pre_analyzed_images
    ) -> [List[ImagePreAnalysis], List[ImagePreAnalysis]]:
        logging.info("Filtering out based on pre analysis")
        valid_pre_analyzed_images = []
        invalid_pre_analyzed_images = []
        for pre_analyzed_image in pre_analyzed_images:
            if pre_analyzed_image.is_valid_picture(self.sort_conditions):
                valid_pre_analyzed_images.append(pre_analyzed_image)
            else:
                invalid_pre_analyzed_images.append(pre_analyzed_image)
        logging.info(f"""
            Filtering process done
            valid: {len(valid_pre_analyzed_images)}
            invalid: {len(invalid_pre_analyzed_images)}
        """)
        return valid_pre_analyzed_images, invalid_pre_analyzed_images

    def _run_inference_on_valid_images(self, valid_pre_analyzed_images) -> List[str]:
        logging.info(f"Inference starting")
        inference = Inference()
        valid_image_paths = [
            valid_pre_analyzed_image.get_path() for valid_pre_analyzed_image in valid_pre_analyzed_images
        ]
        predicted_classes = Parallel(n_jobs=self.num_cores)(
            delayed(inference.get_top_predicted_class)(valid_image_path)
            for valid_image_path in valid_image_paths
        )
        logging.info(f"Inference over")
        return predicted_classes
