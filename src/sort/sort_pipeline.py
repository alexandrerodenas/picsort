import logging
from typing import List

from joblib import Parallel, delayed

from src.inference.inference import Inference, PredictionForPath
from src.load.images_loader import ImageDataLoader
from src.pre_analysis.image_analysis import ImagePreAnalysis
from src.pre_analysis.pre_analyzer import PreAnalyzer
from src.shared.config_reader import AppConfig


class SortPipeline:

    def __init__(self, config: AppConfig):
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

        predictions = self._run_inference_on_valid_images(
            valid_pre_analyzed_images
        )

        (valid_paths_for_predicted_images,
         invalid_paths_for_predicted_images) = self._filter_images_based_on_predicted_class(
            predictions
        )

        invalid_images_paths = (list(map(lambda _: _.get_path(), invalid_pre_analyzed_images))
                                + invalid_paths_for_predicted_images)
        valid_images_paths = (list(map(lambda _: _.get_path(), valid_pre_analyzed_images))
                              + valid_paths_for_predicted_images)

        logging.debug(f"Invalids:{invalid_images_paths}")
        logging.debug(f"Valids: {valid_images_paths}")

        return valid_images_paths, invalid_images_paths

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
        logging.info("Filtering images based on pre analysis")
        valid_pre_analyzed_images = []
        invalid_pre_analyzed_images = []
        for pre_analyzed_image in pre_analyzed_images:
            if pre_analyzed_image.is_valid_picture(self.sort_conditions):
                valid_pre_analyzed_images.append(pre_analyzed_image)
            else:
                invalid_pre_analyzed_images.append(pre_analyzed_image)
        logging.info(f"""
            Filtering process done
            valids: {len(valid_pre_analyzed_images)}
            invalids: {len(invalid_pre_analyzed_images)}
        """)
        return valid_pre_analyzed_images, invalid_pre_analyzed_images

    def _run_inference_on_valid_images(self, valid_pre_analyzed_images) -> List[PredictionForPath]:
        logging.info(f"Inference starting")
        inference = Inference()
        valid_image_paths = [
            valid_pre_analyzed_image.get_path() for valid_pre_analyzed_image in valid_pre_analyzed_images
        ]
        predictions = Parallel(n_jobs=self.num_cores)(
            delayed(inference.get_prediction_for_path)(valid_image_path)
            for valid_image_path in valid_image_paths
        )
        logging.info(f"Inference over")
        return predictions

    def _filter_images_based_on_predicted_class(self, predictions_for_path):
        logging.info("Filtering images based on predicted class")
        valid_paths = []
        invalid_paths = []
        for prediction_for_path in predictions_for_path:
            if prediction_for_path.prediction in self.sort_conditions.trash_classes:
                invalid_paths.append(prediction_for_path.path)
            else:
                valid_paths.append(prediction_for_path.path)
        logging.info(f"""
            Filtering process done
            valids: {len(valid_paths)}
            invalids: {len(invalid_paths)}
        """)
        return valid_paths, invalid_paths
