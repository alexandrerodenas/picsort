import logging
from typing import List, Union

InvalidityReason = Union["blurriness", "text", "white", "nature"]


class PathValidation:
    def __init__(self, path: str, valid: bool, reason: InvalidityReason = None, reason_msg: str = None):
        self.path = path
        self.valid = valid
        self.reason = reason
        self.reason_msg = reason_msg

    def __str__(self):
        status = "Valid" if self.valid else "Invalid"
        reason_str = f", Reason: {self.reason_msg}" if self.reason_msg else ""
        return f"Path: {self.path}, Status: {status}{reason_str}"


class ValidPath(PathValidation):
    def __init__(self, path: str):
        super().__init__(path=path, valid=True)


class InvalidPath(PathValidation):
    def __init__(self, path: str, reason: InvalidityReason, reason_msg: str):
        super().__init__(path=path, valid=False, reason=reason, reason_msg=reason_msg)


class PathValidationsResultPrinter:
    @staticmethod
    def print(path_validations: List[PathValidation]):
        valid_paths = [path_validation for path_validation in path_validations if path_validation.valid]
        invalid_paths = [path_validation for path_validation in path_validations if not path_validation.valid]
        logging.info(f"""
            Validation done
            valids: {len(valid_paths)}
            invalids: {len(invalid_paths)}""")

        PathValidationsResultPrinter._print_valid_paths(valid_paths)
        PathValidationsResultPrinter._print_invalid_paths(invalid_paths)

    @staticmethod
    def _print_invalid_paths(invalid_paths):
        invalid_paths_by_reason = {}
        for invalid_path in invalid_paths:
            reason = invalid_path.reason
            if reason not in invalid_paths_by_reason:
                invalid_paths_by_reason[reason] = []
            invalid_paths_by_reason[reason].append(invalid_path)
        logging.info("Invalid paths:")
        for reason, paths in invalid_paths_by_reason.items():
            logging.info(f"Reason: {reason}")
            for invalid_path in paths:
                logging.info(f"  {invalid_path.path}: {invalid_path.reason_msg}")

    @staticmethod
    def _print_valid_paths(valid_paths):
        logging.info("Valid paths: ")
        for valid_path in valid_paths:
            logging.info(valid_path.path)
