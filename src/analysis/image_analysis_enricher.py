import logging

import cv2
import numpy as np
import pandas as pd
import pytesseract
from joblib import Parallel, delayed

from src.analysis.image_analyzer import ImageAnalyzer

class ImageAnalysisEnricher:

    def __init__(self, analyzer: ImageAnalyzer, num_cores):
        self.analyzer = analyzer
        self.num_cores = num_cores

    def enrich(self, images_dataframe):
        logging.info("Enrichment begins")

        def process_image(row):
            try:
                image_content = row['content']
                white = self.analyzer.get_white_percentage(image_content)
                blur = self.analyzer.get_blur_level(image_content)
                text = self.analyzer.get_text(row["path"]) or "None"
                return white, blur, text
            except Exception as e:
                logging.error(f"An exception occurred with {row['path']}: {str(e)}")
                return None

        results = Parallel(n_jobs=self.num_cores)(
            delayed(process_image)(row) for index, row in images_dataframe.iterrows())
        enrichment = pd.DataFrame(results, columns=['white', 'blur', 'text'])

        logging.info("Enrichment done")

        if len(results) == len(images_dataframe):
            return pd.concat([images_dataframe, enrichment], axis=1)
        else:
            logging.warning("White analysis and image DataFrame lengths do not match.")
