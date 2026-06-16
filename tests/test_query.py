# ruff: noqa: RUF001

import pytest

from tool import query

test_vectors = [
    {
        "input": "わたし",
        "output": ["わたし"],
    },
    {
        "input": "あの人　（あの方）",
        "output": ["あの人", "あの方"],
    },
    {
        "input": "～さん",
        "output": ["さん"],
    },
    {
        "input": "初めまして。",
        "output": ["初めまして"],
    },
    {
        "input": "～から　来ました。",
        "output": ["から来ました"],
    },
    {
        "input": "［どうぞ］　よろしく　［お願いします］。",
        "output": ["どうぞよろしくお願いします"],
    },
    {
        "input": "お名前は？",
        "output": ["お名前は"],
    },
    {
        "input": "",
        "output": [],
    },
]


@pytest.mark.parametrize("vector", test_vectors)
def test_queries(vector: dict) -> None:
    assert query.split(vector["input"]) == vector["output"]
