import unittest
from cp_ecb import read_image, encrypt_image, decrypt_image


class ECBTests(unittest.TestCase):
    def test_sanity(self):
        invert = lambda x: bytes([255 - y for y in x])
        image = read_image("Tux.png", silent=True)
        original = image.b
        inverted = encrypt_image(image, invert, silent=True)
        self.assertTrue(original != inverted.b)
        inverted = decrypt_image(image, invert, silent=True)
        self.assertTrue(original == inverted.b)

if __name__ == '__main__':
    unittest.main()

