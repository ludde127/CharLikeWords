import re
import main.reader
import numpy as np
SPECIAL_CHARACTERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8",
                      "9", "!", "?", "&", ".", ",", ";", ":", "=", "@", "%"]
NUMBER_SPECIAL_CHARACTERS = len(SPECIAL_CHARACTERS)
SEPARATORS = SPECIAL_CHARACTERS[10:17]  # "!", "?", "&", ".", ",", ";", ":"
NOT_SEPARATORS = SPECIAL_CHARACTERS[:10]
NOT_SEPARATORS.extend(SPECIAL_CHARACTERS[17:])

SPECIAL_CHARACTERS_SET = set(SPECIAL_CHARACTERS)
SEPARATORS_SET = set(SEPARATORS)
NOT_SEPARATORS_SET = set(NOT_SEPARATORS)


def allowed_char(char: str):
    return 97 <= ord(char) <= 123 or ord(char) == 32 or char in SPECIAL_CHARACTERS


class TextPreparation:
    def __init__(self):
        deliminators = ["?", "!", ".", ","]

        self.split_regex = re.compile("(" + '|'.join(map(re.escape, deliminators)) + ")")

    @staticmethod
    def remove_non_allowed(text: str):
        return ''.join([i if allowed_char(i) else '' for i in text.lower()]).strip()

    def prepare_sentence(self, text: str) -> list[str]:
        """Returns a list of words of the sentence with each word only consisting of lowercase characters"""
        return [self.remove_non_allowed(word) for word in text.split(" ")]

    def to_sentences(self, text: str):
        """Returns the text split into sentences"""
        sentences = self.split_regex.split(text)
        new_sentences = list()
        for n, sentence in enumerate(sentences):
            if len(sentence) == 1 and n != 0:
                new_sentences[-1] = new_sentences[-1].strip()
                new_sentences[-1] += sentence
            else:
                new_sentences.append(sentence)
        return [sentence for sentence in new_sentences if len(sentence) > 1]

    def prepare(self, text: str) -> list[list[str]]:
        return [self.prepare_sentence(sentence) for sentence in self.to_sentences(text)]


class Compressor(dict):
    def __init__(self):
        super().__init__()
        self.prep = TextPreparation()
        self.map = reader.pairs()  # word -> id map
        del self.map[""]

    def compress_word(self, word: str) -> list[int]:
        if word in self.map:
            return [self.map[word]]
        elif len(word) != 0:
            all_found = list()
            sub = list()
            for c in word:
                if c not in SPECIAL_CHARACTERS:
                    sub.append(c)
                else:
                    all_found.extend(self.compress_word("".join(sub)))
                    all_found.append(self.map[c])
                    sub = list()
            all_found.extend(self.compress_word("".join(sub)))
            return all_found
        else:
            return list()

    def compress_sentence(self, sentence):
        prepared_sentence = self.prep.prepare_sentence(sentence)
        compressed = list()
        for word in prepared_sentence:
            compressed.append(self.compress_word(word))
        return compressed


class DeCompressor(dict):
    def __init__(self):
        super().__init__()
        self.map = {v: k for k, v in reader.pairs().items()}  # id -> word map
        del self.map[24]  # For some reason "" is in here

    def decompress_word(self, compressed_word: list[int]):
        result = ""
        for part in compressed_word:
            result += self.map[part]
        return result

    def decompress_sentence(self, sentence: list[list[int]]):
        return " ".join([self.decompress_word(word) for word in sentence])
