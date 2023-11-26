import logging
from typing import List


class PathValidation:
    def __init__(self, path: str, valid: bool, reason: str = None):
        self.path = path
        self.valid = valid
        self.reason = reason

    def __str__(self):
        status = "Valid" if self.valid else "Invalid"
        reason_str = f", Reason: {self.reason}" if self.reason else ""
        return f"Path: {self.path}, Status: {status}{reason_str}"


class ValidPath(PathValidation):
    def __init__(self, path: str):
        super().__init__(path=path, valid=True)


class InvalidPath(PathValidation):
    def __init__(self, path: str, reason: str):
        super().__init__(path=path, valid=False, reason=reason)


class PathValidationsResultPrinter:
    @staticmethod
    def print(path_validations: List[PathValidation]):
        valid_paths = [path_validation for path_validation in path_validations if path_validation.valid]
        invalid_paths = [path_validation for path_validation in path_validations if not path_validation.valid]
        logging.info(f"""
            Validation done
            valids: {len(valid_paths)}
            invalids: {len(invalid_paths)}""")
        logging.info("Valid paths: ")
        for valid_path in valid_paths:
            logging.info(valid_path.path)
        logging.info("Invalid paths: ")
        for invalid_path in invalid_paths:
            logging.info(f"{invalid_path.path}: {invalid_path.reason}")
