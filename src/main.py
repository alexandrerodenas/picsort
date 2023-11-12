from src.analysis.image_analyzer import SimpleAnalyzer
from src.inference import Inference
from src.shared.config_reader import load_config
from src.analysis.image_analysis_enricher import ImageAnalysisEnricher
from images_loader import ImageDataLoader
from src.shared.file_utils import create_directory, write_dataframe_to_csv
from src.shared.logger import setup_logger

if __name__ == '__main__':
    config = load_config('/../../config.yaml')
    setup_logger(config.logging_level)

    create_directory(config.output_directory)

    dataframe = ImageDataLoader(config.input_directory).get_dataframe()
    dataframe = ImageAnalysisEnricher(
        SimpleAnalyzer(config.analysis_blurriness_threshold, config.tesseract_path),
        config.num_cores
    ).enrich(dataframe)

    dataframe = Inference(config.num_cores).add_predicted_classes(dataframe)

    write_dataframe_to_csv(dataframe, config.output_directory)

