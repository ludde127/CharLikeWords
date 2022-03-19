import unittest
from main import DeCompressor, Compressor


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.d = DeCompressor()
        self.c = Compressor()

    def test_compress_decompress_word(self):
        self.assertEqual(self.d.decompress_word(self.c.compress_word("!test")), '!test')

        self.assertEqual(self.d.decompress_word(self.c.compress_word("te!st")), "te!st")
        self.assertEqual(self.d.decompress_word(self.c.compress_word("te?st")), 'te?st')
        self.assertEqual(self.d.decompress_word(self.c.compress_word("test?")), 'test?')
        self.assertEqual(self.d.decompress_word(self.c.compress_word("!intel?")), '!intel?')

    def test_compress_sentence(self):
        test_sentence = "This is a test sentence, will this work at all?"
        self.assertEqual(self.d.decompress_sentence(self.c.compress_sentence(test_sentence)), test_sentence.lower())

        test_sentence = "Writing tests are kind of annoying, ill do one more after this one."
        self.assertEqual(self.d.decompress_sentence(self.c.compress_sentence(test_sentence)), test_sentence.lower())

        test_sentence = "boy am i getting bored of writing these."
        self.assertEqual(self.d.decompress_sentence(self.c.compress_sentence(test_sentence)), test_sentence.lower())


if __name__ == '__main__':
    unittest.main()
