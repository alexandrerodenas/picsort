import logging

import pandas as pd
from joblib import Parallel, delayed

from src.analysis.image_analyzer import ImageAnalyzer
from src.shared.dataframe_utils import vertical_concat


class ImageAnalysisEnricher:

    def __init__(self, analyzer: ImageAnalyzer, num_cores):
        self.analyzer = analyzer
        self.num_cores = num_cores

    def enrich(self, images_dataframe):
        logging.info("Enrichment begins")
        results = Parallel(n_jobs=self.num_cores)(
            delayed(self._process_image)(row) for index, row in images_dataframe.iterrows())
        enrichment = pd.DataFrame(results, columns=['white', 'blur', 'text'])
        logging.info("Enrichment done")
        return vertical_concat(images_dataframe, enrichment)

    def _process_image(self, row):
        try:
            image_grayscale = row['grayscale']
            white = self.analyzer.get_white_percentage(image_grayscale)
            blur = self.analyzer.get_blur_level(image_grayscale)
            text = self.analyzer.get_text(row["path"]) or "None"
            return white, blur, text
        except Exception as e:
            logging.error(f"An exception occurred with {row['path']}: {str(e)}")
            return None