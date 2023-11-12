class ImagePreAnalysis:
    def __init__(self, path: str, blurriness: int, white_percentage: int, text: str):
        self.blurriness = blurriness
        self.white_percentage = white_percentage
        self.text = text
        self.path = path

    def is_invalid_picture(self, blurriness_threshold, white_percentage_threshold):
        return (len(self.text) > 0
                or self.blurriness > blurriness_threshold
                or self.white_percentage > white_percentage_threshold)