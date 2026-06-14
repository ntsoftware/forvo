import logging

from tool import WordList


def test_words1():
    wl = WordList("test-input/words1.txt")
    for row in wl:
        logging.info(row)
    wl.save("test-output/words1.txt")


def test_words2():
    wl = WordList("test-input/words2.txt")
    for row in wl:
        logging.info(row)
    wl.save("test-output/words2.txt")


def test_words3():
    wl = WordList("test-input/words3.txt")
    for row in wl:
        logging.info(row)
    wl.save("test-output/words3.txt")
