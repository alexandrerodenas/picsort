import concurrent.futures
import logging
from typing import Hashable

import cv2
import numpy as np
import pandas as pd
from joblib import Parallel, delayed


class PixelAnalysis:

    @staticmethod
    def _get_white_percentage(image_content):
        image = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_GRAYSCALE)
        n_white_pix = np.sum(image == 255)
        return int((n_white_pix / image.size) * 100)

    def enriched(self, images_dataframe):
        logging.info("Computing percentage of white in images")

        def process_image(row):
            try:
                white = self._get_white_percentage(row["content"])
                blur = self._get_blur_percentage(row['content'])
                return white, blur
            except Exception as e:
                logging.error(f"An exception occurred with {row['path']}: {str(e)}")
                return None

        num_cores = 4
        results = Parallel(n_jobs=num_cores)(delayed(process_image)(row) for index, row in images_dataframe.iterrows())
        pixel_analysis = pd.DataFrame(results, columns=['white', 'blur'])

        logging.info("Computing done")

        if len(results) == len(images_dataframe):
            return pd.concat([images_dataframe, pixel_analysis], axis=1)
        else:
            logging.warning("White analysis and image DataFrame lengths do not match.")

    @staticmethod
    def _get_blur_percentage(image_content):
        try:
            image = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_GRAYSCALE)
            laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
            threshold = 100

            if laplacian_var < threshold:
                blur_percentage = 100
            else:
                blur_percentage = 0

            return blur_percentage

        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
