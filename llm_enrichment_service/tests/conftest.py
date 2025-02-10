import os
import pytest

@pytest.fixture
def load_from_data_dir():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Now points to tests/
    DATA_DIR = os.path.join(BASE_DIR, "data")
    def _load_file(filename):
        file_path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{filename}' not found in data/ directory")

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    return _load_file