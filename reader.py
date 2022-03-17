import csv
import numpy as np
file = "word_data.csv"


def pairs():
    """Loads the data as a list of (id, word, frequency) tuples"""

    def into_uint32(_id, word, frequency):
        # uint32 should take up way less memory than python integers.
        return np.uint32(_id), word, np.uint32(frequency)

    with open(file, "r") as f:
        reader = csv.reader(file)
        data = list(reader)
    data = [into_uint32(*d) for d in data]
    return data
