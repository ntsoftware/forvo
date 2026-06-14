import logging
from pathlib import Path

import pytest

from tool import Config, WordList

test_vectors = [
    {
        "input": "test-input/words1.txt",
        "output": "test-output/words1.txt",
    },
    {
        "input": "test-input/words2.txt",
        "output": "test-output/words2.txt",
    },
    {
        "input": "test-input/words3.txt",
        "output": "test-output/words3.txt",
    },
]


@pytest.fixture
def cfg() -> Config:
    return Config()


@pytest.mark.parametrize("vector", test_vectors)
def test_read_write(vector, cfg):
    input_file = Path(vector["input"])
    output_file = Path(vector["output"])

    wl = WordList(input_file, cfg)
    for row in wl:
        logging.info(row)
    wl.save(output_file)

    assert input_file.read_bytes() == output_file.read_bytes()
