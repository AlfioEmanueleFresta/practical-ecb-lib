import unittest
from cp_ecb import read_image, encrypt_image, decrypt_image,\
                   get_ecb_encrypter, get_stream_cipher, encrypt_image_file


SOURCE_IMAGE = "examples/tux.png"


class ECBTests(unittest.TestCase):

    def test_sanity(self):
        invert = lambda x: bytes([255 - y for y in x])
        image = read_image("Tux.png", silent=True)
        original = image.b
        inverted = encrypt_image(image, invert, silent=True)
        self.assertTrue(original != inverted.b)
        inverted = decrypt_image(image, invert, silent=True)
        self.assertTrue(original == inverted.b)

    def test_make_ecb(self):
        key = "My secret key"
        encrypter = get_ecb_encrypter(key)
        encrypt_image_file(SOURCE_IMAGE, encrypter, "examples/ecb.png")
        # TODO Decrypt and check for similarity

    def test_make_otp(self):
        cipher = get_stream_cipher(seed="My secret seed")
        encrypt_image_file(SOURCE_IMAGE, cipher, "examples/otp.png")
        # TODO Decrypt and check for similarity

    def test_make_invert(self):
        inverter = lambda image: bytes([0xff - pixel for pixel in image])
        encrypt_image_file(SOURCE_IMAGE, inverter, "examples/inverted.png")
        # TODO Decrypt and check for similarity

if __name__ == '__main__':
    unittest.main()

