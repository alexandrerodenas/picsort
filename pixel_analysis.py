import concurrent.futures
import logging
from typing import Hashable

import cv2
import numpy as np
from joblib import Parallel, delayed


class PixelAnalysis:

    @staticmethod
    def _get_white_percentage(image_content):
        image = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_GRAYSCALE)
        n_white_pix = np.sum(image == 255)
        return (n_white_pix / image.size) * 100

    def enriched_with_white_analysis(self, images_dataframe):
        logging.info("Computing percentage of white in images")

        def process_image(row):
            try:
                return self._get_white_percentage(row["content"])
            except Exception as e:
                logging.error(f"An exception occurred with {row['path']}: {str(e)}")
                return None

        num_cores = 4
        results = Parallel(n_jobs=num_cores)(delayed(process_image)(row) for index, row in images_dataframe.iterrows())

        if len(results) == len(images_dataframe):
            images_dataframe["white"] = results
        else:
            logging.warning("White analysis and image DataFrame lengths do not match.")

        logging.info("Computing done")
        return images_dataframe
