from src.shared.config_reader import SortConditions


class ImagePreAnalysis:
    def __init__(self, path: str, blurriness: int, white_percentage: int, text: str):
        self.blurriness = blurriness
        self.white_percentage = white_percentage
        self.text = text
        self.path = path

    def get_path(self):
        return self.path

    def is_valid_picture(self, sort_conditions: SortConditions):
        return (
                len(self.text) <= sort_conditions.text_threshold
                or self.blurriness <= sort_conditions.blurriness_threshold
                or self.white_percentage <= sort_conditions.white_percentage_threshold
        )