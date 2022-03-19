import pickle

import numpy as np


def pairs():
    """Loads the data as a list of (id, word) tuples"""

    file = "C:/Users/ludvi/PycharmProjects/CharLikeWords/main/small.pkl"

    def read_obj():
        with open(file, "rb") as f:
            data = pickle.load(f)
        return data

    return read_obj()
