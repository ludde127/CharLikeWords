import reader


class Compressor(dict):
    def __init__(self, minimum_frequency=0):
        super().__init__()
        self.minimum_frequency = minimum_frequency

        data = reader.pairs()  # (id, word, frequency)
        self.update({e[1]: e[0] for e in data if data[2] > minimum_frequency})


class DeCompressor(dict):
    def __init__(self, minimum_frequency=0):
        super().__init__()
        self.minimum_frequency = minimum_frequency

        data = reader.pairs()  # (id, word, frequency)
        self.update({e[0]: e[1] for e in data if data[2] > minimum_frequency})
